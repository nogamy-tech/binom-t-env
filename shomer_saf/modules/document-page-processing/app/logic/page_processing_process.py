from app.logic.utils.config import load_config, create_config_file
from app.logic.utils.services.document_ai import DocumentAIClient, custom_errors as de
from app.logic.utils.services.storage import Gcs, custom_errors as se
from app.logic.utils.services import GCPServiceFactory
from app.logic.utils.src.preprocessing_pipeline import preprocess_text, preprocess_image
from app.logic.utils.services.logging import ExecutionLogger
import base64

main_logger = ExecutionLogger(customer_id="document-page-process")


class PageProcessingProcess:
    """
    Main processing class for document page processing.
    """

    @staticmethod
    def run_process(msg) -> tuple[int, str]:
        """
        Process a single document page using the specified model.

        Args:
            msg (DocumentPageProcessingRequest):
                Pydantic object containing:
                    - PageNumber (int)
                    - Model (str)
                    - DnaTransactionId (str)
                    - DataBucketFolder (str)
                    - PagesBucketFolder (str)
                    - BucketSubPath (str)

        Returns:
            tuple[int, str]: (error_code, message) where 200="OK" indicates success
        """
        return PageProcessingProcess.main_page_processor(
            PageNumber=msg.get("PageNumber"),
            Model=msg.get("Model"),
            DnaTransactionId=msg.get("DnaTransactionId"),
            DataBucketFolder=msg.get("DataBucketFolder"),
            PagesBucketFolder=msg.get("PagesBucketFolder"),
            BucketSubPath=msg.get("BucketSubPath"),
        )

    @staticmethod
    @main_logger.log_execution
    def main_page_processor(
        PageNumber: int,
        Model: str,
        DnaTransactionId: str,
        DataBucketFolder: str,
        PagesBucketFolder: str,
        BucketSubPath: str,
    ) -> tuple[int, str, str]:
        """
        Processes a single page from GCS, runs it through a Document AI model,
        and uploads the result back to GCS.

        Args:
            PageNumber (int): Page number to process.
            Model (str): Type of processing: "text" or "image".
            DnaTransactionId (str): Transaction identifier for the document.
            DataBucketFolder (str): GCS bucket for storing processed results.
            PagesBucketFolder (str): GCS bucket where source pages are stored.
            BucketSubPath (str): Subfolder path inside the buckets.

        Returns:
            Tuple[int, str, str]: (RequestErrorCode, RequestErrorMessage, output_path)
                - output_path: GCS path to the processed file if successful, empty string on error.

        Notes:
            - Handles errors for missing buckets/blobs, AI processing failures, and timeouts.
            - Text outputs are saved as Markdown (.md), image outputs as TIFF (.tiff).
        """

        gcp_service_factory = GCPServiceFactory()
        create_config_file(gcp_service_factory=gcp_service_factory)
        config = load_config()

        blob_name = (
            f"{PagesBucketFolder}/{BucketSubPath}/{DnaTransactionId}/{PageNumber}.tiff"
        )
        main_bucket = config["project"]["bucket"]
        ministry_name, project_name, client_request_id = DnaTransactionId.split("_")
        main_logger.set_context(
            customer_id=client_request_id,
            ministry_name=ministry_name,
            project_name=project_name,
            dna_transaction_id=DnaTransactionId,
        )
        main_logger.logger.info(f"Start document-page-process for: {blob_name}")

        try:
            gcs_service = Gcs(
                gcp_service_factory=gcp_service_factory, bucket_name=main_bucket
            )
            tiff_bytes = gcs_service.read_gcs_file(blob_name=blob_name)

        except se.BucketNotFound:
            main_logger.logger.exception(f"Bucket not exists: {blob_name}")
            RequestErrorCode, RequestErrorMessage = 461, "BUCKET_NOT_EXISTS"
            return RequestErrorCode, RequestErrorMessage, ""

        except se.BucketTimeOut:
            main_logger.logger.exception(f"Bucket timeout: {blob_name}")
            RequestErrorCode, RequestErrorMessage = 462, "BUCKET_TIMEOUT"
            return RequestErrorCode, RequestErrorMessage, ""

        except se.BlobNotFound:
            main_logger.logger.exception(f"No document in bucket: {blob_name}")
            RequestErrorCode, RequestErrorMessage = 463, "NO_DOCUMENT_IN_BUCKET"
            return RequestErrorCode, RequestErrorMessage, ""

        except se.MultipleFilesFound:
            main_logger.logger.exception(f"No document in bucket: {blob_name}")
            RequestErrorCode, RequestErrorMessage = 463, "NO_DOCUMENT_IN_BUCKET"
            return RequestErrorCode, RequestErrorMessage, ""

        base64_input = base64.b64encode(tiff_bytes).decode("utf-8")

        docai_client = DocumentAIClient(
            location=config["project"]["location"],
            processor_id=config["project"]["processor_id"],
            gcp_factory=gcp_service_factory,
        )

        if Model.lower() == "text":
            try:
                base64_output = preprocess_text(
                    docai_client=docai_client,
                    file_base64=base64_input,
                    mime_type="image/tiff",
                )

                # Convert base64 to text
                decoded_bytes = base64.b64decode(base64_output)
                text_content = decoded_bytes.decode("utf-8")

                # define destination blob path
                destination_blob_name = f"{DataBucketFolder}/{BucketSubPath}/{DnaTransactionId}/{PageNumber}.md"

                gcs_service.upload_to_gcs(
                    destination_blob_name=destination_blob_name,
                    source_file_text=text_content,
                    content_type="text/markdown",
                )

            except de.DocumentAIFailure:
                main_logger.logger.exception(f"Document AI failure: {blob_name}")
                RequestErrorCode, RequestErrorMessage = 464, "DOCUMENT_AI_FAILURE"
                return RequestErrorCode, RequestErrorMessage, ""

            except de.DocumentAITimeout:
                main_logger.logger.exception(f"Document AI timeout: {blob_name}")
                RequestErrorCode, RequestErrorMessage = 465, "DOCUMENT_AI_TIMEOUT"
                return RequestErrorCode, RequestErrorMessage, ""

        elif Model.lower() == "image":
            try:
                base64_output = preprocess_image(
                    docai_client=docai_client,
                    file_base64=base64_input,
                    mime_type="image/tiff",
                )

                # Convert base64 to bytes
                decoded_bytes = base64.b64decode(base64_output)

                # define destination blob path
                destination_blob_name = f"{DataBucketFolder}/{BucketSubPath}/{DnaTransactionId}/{PageNumber}.tiff"

                gcs_service.upload_to_gcs(
                    bucket_name=main_bucket,
                    destination_blob_name=destination_blob_name,
                    source_file_bytes=decoded_bytes,
                )

            except de.ImgQualityInvalid:
                main_logger.logger.exception(f"Image quality invalid: {blob_name}")
                RequestErrorCode, RequestErrorMessage = 466, "IMAGE_QUALITY_INVALID"
                return RequestErrorCode, RequestErrorMessage, ""

        # define final response if everything works as expected
        path = f"{main_bucket}/{destination_blob_name}"
        RequestErrorCode, RequestErrorMessage = 200, "OK"
        print(RequestErrorCode, RequestErrorMessage, path)

        return RequestErrorCode, RequestErrorMessage, path
