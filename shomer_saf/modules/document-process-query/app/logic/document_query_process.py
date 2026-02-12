from datetime import datetime
from .utils.services import GCPServiceFactory
from .utils.services.vertex_ai import LLM, LLMResponse, custom_errors as ve
from .utils.services.storage import Gcs, custom_errors as se
from .utils.config import create_config_file, load_config
from .utils.services.firestore import FirestoreClient
from app.logic.utils.services.logging import ExecutionLogger

main_logger = ExecutionLogger(customer_id="document-process-query")

class DocumentQueryProcess:
    """
    Main processing class for FastInspector document validation.
    """

    @staticmethod
    def run_process(msg) -> tuple[int, str, LLMResponse]:
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
            tuple[int, str]: (error_code, message) where 202="OK" indicates success
        """
        return DocumentQueryProcess.main_llm_query(
            DnaTransactionId=msg.get("DnaTransactionId"), PageNumber=msg.get("PageNumber"), Query=msg.get("Query"), DataBucketFolder=msg.get("DataBucketFolder"), BucketSubPath=msg.get("BucketSubPath")
        )

    @staticmethod
    @main_logger.log_execution
    def main_llm_query(DnaTransactionId: str, PageNumber: int, Query: dict[str, str], DataBucketFolder: str, BucketSubPath: str) -> tuple[int, str, LLMResponse]:
        """
        Processes a single page from GCS using a specified LLM model (text or image)
        and writes the response to Firestore.

        Args:
            DnaTransactionId (str): Document transaction identifier.
            PageNumber (int): Page number to process.
            Query (Dict[str, str]): User query containing 'model' and 'query' keys.
            DataBucketFolder (str): GCS bucket storing the source files.
            BucketSubPath (str): Subfolder path inside the GCS bucket.

        Returns:
            Tuple[int, str, LLMResponse]:
                - HTTP-like status code (int)
                - Request error code/message (str)
                - LLMResponse object containing the model's answer.
        """
        gcp_service_factory = GCPServiceFactory()
        create_config_file(gcp_service_factory=gcp_service_factory)
        config = load_config()

        RequestErrorCode, RequestErrorMessage, final_llm_answer = 200, "OK", None
        # 0. get user's query and model type (image/text)
        model_type = Query.get("model").lower()
        user_query = Query.get("query")
        query_id = Query.get("id")
        main_bucket = config["project"]["bucket"]
        ministry_name, project_name, client_request_id = DnaTransactionId.split("_")
        sub_req_id = f"{DnaTransactionId}_{PageNumber}_{Query.get('id','')}"
        main_logger.set_context(customer_id=client_request_id,ministry_name=ministry_name,project_name=project_name,dna_transaction_id=DnaTransactionId)
        main_logger.logger.info(f"Start document-process-query for {sub_req_id}")

        try:
            gcs_service = Gcs(gcp_service_factory=gcp_service_factory, bucket_name=main_bucket)
            llm = LLM(
                gcp_factory=gcp_service_factory,
                prompt_path=config["paths"]["prompt_path"],
                text_model_name=config["project"]["text_model_name"],
                image_model_name=config["project"]["image_model_name"],
            )

            file_ext = "tiff" if model_type == "image" else "md"
            # 1.set blob name with 'tiff' ending
            blob_name = f"{DataBucketFolder}/{BucketSubPath}/{DnaTransactionId}/{PageNumber}.{file_ext}"
            # 2.read content - expect bytes
            file_content = gcs_service.read_gcs_file(blob_name=blob_name)

            if model_type == "image" and not isinstance(file_content, bytes):
                RequestErrorCode, RequestErrorMessage, final_llm_answer = 470, "MODEL_FAILURE", None

            if model_type == "text" and not isinstance(file_content, str):
                RequestErrorCode, RequestErrorMessage, final_llm_answer = 470, "MODEL_FAILURE", None

            # 3.get llm answer from file content + user's query
            llm_answer = llm.query(user_query=user_query, context=file_content)
            final_llm_answer = llm_answer.model_dump()

            # handle whether the llm's output is not boolean
            if not isinstance(llm_answer.final_answer, bool):
                RequestErrorCode, RequestErrorMessage, final_llm_answer = 470, "MODEL_FAILURE", None
                print("The model's final answer is not boolean")

        # 4. handle EXCEPTIONS
        except se.BucketNotFound:
            main_logger.logger.exception(f"Bucket not exists: {sub_req_id}")
            RequestErrorCode, RequestErrorMessage = 461, "BUCKET_NOT_EXISTS"

        except se.BucketTimeOut:
            main_logger.logger.exception(f"Bucket timeout: {sub_req_id}")
            RequestErrorCode, RequestErrorMessage = 462, "BUCKET_TIMEOUT"

        except se.BlobNotFound:
            main_logger.logger.exception(f"Data missing: {sub_req_id}")
            RequestErrorCode, RequestErrorMessage = 463, "DATA_MISSING"

        except ve.VisionModelTimeOut:
            main_logger.logger.exception(f"Vision model timeout: {sub_req_id}")
            RequestErrorCode, RequestErrorMessage = 464, "VISION_MODEL_TIMEOUT"
            print(f"Timeout while processing {model_type} model.")

        except ve.TextModelTimeOut:
            main_logger.logger.exception(f"Text model timeout: {sub_req_id}")
            RequestErrorCode, RequestErrorMessage = 465, "TEXT_MODEL_TIMEOUT"
            print(f"Timeout while processing {model_type} model.")

        except ve.ModelFailure:
            main_logger.logger.exception(f"Model failure: {sub_req_id}")
            RequestErrorCode, RequestErrorMessage = 466, "MODEL_FAILURE"
            print(f"Timeout while processing {model_type} model.")

        except Exception as e:
            main_logger.logger.exception(f"Model failure: {sub_req_id}")
            RequestErrorCode, RequestErrorMessage = 466, "MODEL_FAILURE"
            print(f"Unexpected error in {model_type} model:", e)

        # update firestore
        db_dict = {
            "DnaTransactionId": DnaTransactionId,
            "Page_number": int(PageNumber),
            "Query_number": int(query_id),
            "Query": user_query,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "QueryResponse": final_llm_answer,
            "RequestErrorCode": RequestErrorCode,
            "RequestErrorMessage": RequestErrorMessage,
            "status": "Ended_DocumentProcessQuery",
        }

        firestore = FirestoreClient(gcp_service_factory=gcp_service_factory, db_name=config["project"]["db_name"], collection_name=config["project"]["collection_name"])
        firestore.set_collection(config["project"]["collection_name"])
        firestore.set_internal_id(f"{DnaTransactionId}_{PageNumber}_{query_id}")
        firestore.write_llm_answer_to_db(**db_dict)

        print(RequestErrorCode, RequestErrorMessage, final_llm_answer)

        return RequestErrorCode, RequestErrorMessage, final_llm_answer
