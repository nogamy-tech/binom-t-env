from app.logic.utils.config import load_config, create_config_file
from app.logic.utils.services.storage import Gcs, custom_errors as ce
from app.logic.utils.src.preprocessing import split_file_to_pages, convert_to_tiff
from app.logic.utils.services import GCPServiceFactory
from app.logic.utils.services.logging import ExecutionLogger

main_logger = ExecutionLogger(customer_id="document-pre-process")

class DocumentPreProcessingProcess:
    """
    Main processing class for FastInspector document validation.
    """

    @staticmethod
    def run_process(msg) -> tuple[int, str]:
        """
        Process a document from GCS into individual page images.

        Args:
            msg: DocumentPreProcessingRequest containing DnaTransactionId, DocumentsBucketFolder,
                PagesBucketFolder, and BucketSubPath

        Returns:
            tuple[int, str]: (error_code, message) where 202="OK" indicates success
        """
        return DocumentPreProcessingProcess.main_preprocessor(
            DnaTransactionId=msg.get("DnaTransactionId"),
            DocumentsBucketFolder=msg.get("DocumentsBucketFolder"),
            PagesBucketFolder=msg.get("PagesBucketFolder"),
            BucketSubPath=msg.get("BucketSubPath"),
        )

    @staticmethod
    @main_logger.log_execution
    def main_preprocessor(
        DnaTransactionId: str,
        DocumentsBucketFolder: str,
        PagesBucketFolder: str,
        BucketSubPath: str,
    ) -> tuple[str, str]:
        """
        Orchestrates the preprocessing of a document from GCS into page images.

        Retrieves a document blob from the `DocumentsBucketFolder`, splits it
        into individual pages, converts each page to TIFF format, and uploads
        them to the `PagesBucketFolder` under the specified subpath.

        Args:
            DnaTransactionId: Unique transaction/document identifier (also blob name).
            DocumentsBucketFolder: GCS bucket containing the source documents.
            PagesBucketFolder: GCS bucket where processed page images are stored.
            BucketSubPath: Subfolder path inside the buckets.

        Returns:
            Tuple[str, str]: A tuple of (error_code, message), where "202, OK"
            indicates success and other codes describe specific errors.

        Error Codes:
            461: BUCKET_NOT_EXISTS – Source or destination bucket not found.
            462: BUCKET_TIMEOUT – GCS request timed out.
            463: NO_DOCUMENT_IN_BUCKET – Document blob missing or multiple files found.
            202: OK – Processing and upload completed successfully.
        """
        ministry_name, project_name, client_request_id = DnaTransactionId.split("_")
        main_logger.set_context(customer_id=client_request_id,ministry_name=ministry_name,project_name=project_name,dna_transaction_id=DnaTransactionId)
        main_logger.logger.info(f"Start document-pre-process")
        gcp_service_factory = GCPServiceFactory()
        create_config_file(gcp_service_factory=gcp_service_factory)
        config = load_config()
        main_bucket = config["project"]["bucket"]

        try:
            gcs_service = Gcs(gcp_service_factory=gcp_service_factory,bucket_name=main_bucket)
            file_bytes, file_type = gcs_service.process_blob_from_gcs(
                sub_folder=f"{DocumentsBucketFolder}/{BucketSubPath}/{DnaTransactionId}",
                blob_name="document",
            )

        except ce.BucketNotFound:
            main_logger.logger.exception(f"Bucket not exists")
            RequestErrorCode, RequestErrorMessage = 461, "BUCKET_NOT_EXISTS"
            return RequestErrorCode, RequestErrorMessage

        except ce.BucketTimeOut:
            main_logger.logger.exception(f"Bucket timeout")
            RequestErrorCode, RequestErrorMessage = 462, "BUCKET_TIMEOUT"
            return RequestErrorCode, RequestErrorMessage

        except ce.BlobNotFound:
            main_logger.logger.exception(f"No document in bucket")
            RequestErrorCode, RequestErrorMessage = 463, "NO_DOCUMENT_IN_BUCKET"
            return RequestErrorCode, RequestErrorMessage

        except ce.MultipleFilesFound:
            main_logger.logger.exception(f"No document in bucket")
            RequestErrorCode, RequestErrorMessage = 463, "NO_DOCUMENT_IN_BUCKET"
            return RequestErrorCode, RequestErrorMessage

        pages = split_file_to_pages(file_bytes=file_bytes, file_type=file_type)

        # each page is converted to tiff bytes - and uploaded to GCS Buckets
        for page_number, page in enumerate(pages):
            page_bytes = convert_to_tiff(page)

            destination_blob_name = f"{PagesBucketFolder}/{BucketSubPath}/{DnaTransactionId}/{page_number}.tiff"

            try:
                gcs_service.upload_to_gcs(
                    destination_blob_name=destination_blob_name,
                    source_file_bytes=page_bytes,
                )

            except ce.BucketNotFound:
                main_logger.logger.exception(f"Bucket for tiff not exists")
                RequestErrorCode, RequestErrorMessage = 461, "BUCKET_NOT_EXISTS"
                return RequestErrorCode, RequestErrorMessage

            except ce.BucketTimeOut:
                main_logger.logger.exception(f"Bucket for tiff timeout")
                RequestErrorCode, RequestErrorMessage = 462, "BUCKET_TIMEOUT"
                return RequestErrorCode, RequestErrorMessage

        RequestErrorCode, RequestErrorMessage = 200, "OK"
        print(RequestErrorCode, RequestErrorMessage)
        return RequestErrorCode, RequestErrorMessage
