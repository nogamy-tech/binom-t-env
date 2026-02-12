"""
Main processing logic for Document Start Job.
"""

from typing import Dict, Tuple
from datetime import datetime
import uuid
from .utils.services import GCPServiceFactory

from .utils.services.storage import Gcs, custom_errors as se
from .utils.config import create_config_file, load_config
from .utils.services.firestore import FirestoreClient
from .utils.src.accounts_db import query_accounts_db, AccountsDBTimeout, UnknownClient

# from .utils.src.logging import log_to_cloud_logging
from .utils.src.document_query_response import (
    update_record_with_error,
    delete_existing_records,
    DocumentQueryResponseTimeout,
    create_document_record,
    create_query_records,
    create_page_records,
)
from .utils.src.document_validation import (
    validate_document,
    UnsupportedFormat,
    UnreadableFile,
)
from .utils.services.workflow import Workflow, WorkflowTimeout, WorkflowError
from app.logic.utils.services.logging import ExecutionLogger

main_logger = ExecutionLogger(customer_id="document-start-job")


class DocumentStartJobProcess:
    """
    Main processing class for Document Start Job.
    """

    @staticmethod
    def run_process(msg: Dict) -> Tuple[int, str]:
        """
        Process a document start job request.

        Args:
            msg: Dictionary containing request data with:
                - ClientRequestId: str
                - Document: str (base64)
                - Queries: List[Dict]
                - x_client_id: str
                - x_client_secret: str (optional)
                - x_scope: str

        Returns:
            tuple[int, str]: (error_code, message) where 202="OK" indicates success
        """
        return DocumentStartJobProcess.main_process(
            client_request_id=msg.get("ClientRequestId"),
            document_base64=msg.get("Document"),
            queries=msg.get("Queries"),
            x_client_id=msg.get("x_client_id"),
            x_client_secret=msg.get("x_client_secret"),
            x_scope=msg.get("x_scope"),
        )

    @staticmethod
    @main_logger.log_execution
    def main_process(
        client_request_id: str,
        document_base64: str,
        queries: list,
        x_client_id: str,
        x_client_secret: str,
        x_scope: str,
    ) -> Tuple[int, str]:
        """
        Main processing logic for Document Start Job.

        Returns:
            Tuple[int, str]: (error_code, error_message)
        """
        # Generate a unique request ID and a current timestamp
        request_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        # * Step 1: Input Schema Validation (already done by Pydantic)
        # If we reach here, schema is valid

        main_logger.logger.info(f"Start document-start-job for: {client_request_id}")
        gcp_service_factory = GCPServiceFactory()
        create_config_file(gcp_service_factory=gcp_service_factory)
        config = load_config()

        # define service clients
        workflow_client = Workflow(
            gcp_service_factory=gcp_service_factory,
            project_id=gcp_service_factory.get_projectid(),
            region=config["project"]["region"],
        )
        data_db = FirestoreClient(
            gcp_service_factory=gcp_service_factory,
            db_name=config["project"]["db_name"],
            collection_name=config["project"]["collection_name"],
        )
        accounts_db = FirestoreClient(
            gcp_service_factory=gcp_service_factory,
            db_name=config["project"]["accounts_db"],
            collection_name=config["project"]["accounts_collection"],
        )

        # * Step 2: Query AccountsDB
        try:
            data = query_accounts_db(
                db_client=accounts_db, x_client_id=x_client_id, x_scope=x_scope
            )
            ministry_name = data.get("MinistryName")
            project_name = data.get("ProjectName")
            bucket_sub_path = data.get("bucket_sub_path")

        except AccountsDBTimeout as e:
            main_logger.logger.exception(f"AccountsDB timeout: {e}")
            update_record_with_error(
                data_db, client_request_id, 424, "ACCOUNTS_DB_TIMEOUT"
            )
            return 424, "ACCOUNTS_DB_TIMEOUT"
        except UnknownClient as e:
            main_logger.logger.exception(f"Unknown client: {e}")
            update_record_with_error(data_db, client_request_id, 460, "UNKNOWN_CLIENT")
            return 460, "UNKNOWN_CLIENT"

        # Generate DnaTransactionId
        dna_transaction_id = f"{ministry_name}_{project_name}_{client_request_id}"
        ministry_name, project_name, client_request_id = dna_transaction_id.split("_")
        main_logger.set_context(
            customer_id=client_request_id,
            ministry_name=ministry_name,
            project_name=project_name,
            dna_transaction_id=dna_transaction_id,
        )

        # * Step 3: Validate document
        try:
            document_bytes, file_type, page_count = validate_document(
                document_base64=document_base64
            )
        except UnsupportedFormat as e:
            main_logger.logger.exception(f"Unsupported format: {e}")
            update_record_with_error(
                data_db, dna_transaction_id, 431, "UNSUPPORTED_FORMAT"
            )
            return 431, "UNSUPPORTED_FORMAT"
        except UnreadableFile as e:
            main_logger.logger.exception(f"Unreadable file: {e}")
            update_record_with_error(
                data_db, dna_transaction_id, 432, "UNREADABLE_FILE"
            )
            return 432, "UNREADABLE_FILE"

        # * Step 4: Load Params for configuration
        documents_bucket_folder = config["project"]["documents_bucket"]
        pages_bucket_folder = config["project"]["pages_bucket"]
        data_bucket_folder = config["project"]["data_bucket"]
        main_bucket = config["project"]["bucket"]
        workflow_name = config["project"]["workflow_name"]

        # * Step 5: Check DocumentsBucketFolder existance
        try:
            bucket_client = Gcs(
                gcp_service_factory=gcp_service_factory, bucket_name=main_bucket
            )
        except se.BucketNotFound as e:
            main_logger.logger.exception(f"Bucket not found: {e}")
            update_record_with_error(
                data_db, dna_transaction_id, 461, "BUCKET_NOT_EXISTS"
            )
            return 461, "BUCKET_NOT_EXISTS"

        except se.BucketTimeOut as e:
            main_logger.logger.exception(f"Bucket timeout: {e}")
            update_record_with_error(data_db, dna_transaction_id, 462, "BUCKET_TIMEOUT")
            return 462, "BUCKET_TIMEOUT"

        # * Step 6: Check if folder exists and handle overwrite
        folder_path = (
            f"{documents_bucket_folder}/{bucket_sub_path}/{dna_transaction_id}"
        )

        # Check if folder exists (by checking if any blob exists with this prefix)
        if bucket_client.count_blobs_in_subfolder(subfolder_prefix=folder_path) > 0:
            # Check if workflow is running
            if workflow_client.check_workflow_running(
                workflow_name=workflow_name,
                filter_key="DnaTransactionId",
                filter_value=dna_transaction_id,
            ):
                main_logger.logger.exception(
                    "ClientRequestId already used and workflow running"
                )
                update_record_with_error(
                    data_db, dna_transaction_id, 463, "CLIENT_REQUEST_ID_ALREADY_USED"
                )
                return 463, "CLIENT_REQUEST_ID_ALREADY_USED"

            # Delete existing records
            try:
                delete_existing_records(
                    db_client=data_db, dna_transaction_id=dna_transaction_id
                )
            except DocumentQueryResponseTimeout as e:
                main_logger.logger.exception(f"DB timeout deleting records: {e}")
                update_record_with_error(data_db, dna_transaction_id, 424, "DB_TIMEOUT")
                return 424, "DB_TIMEOUT"

            # Delete existing blobs in folder (overwrite)
            try:
                blobs = list(bucket_client.bucket.list_blobs(prefix=folder_path))
                for blob in blobs:
                    blob.delete()

            except Exception as e:
                main_logger.logger.exception(f"Error deleting existing blobs: {e}")

        # * Step 7: Upload document to bucket
        destination_blob_name = f"{folder_path}/document"

        try:
            content_type_map = {
                "pdf": "application/pdf",
                "jpeg": "image/jpeg",
                "jpg": "image/jpeg",
                "png": "image/png",
            }
            bucket_client.upload_to_gcs(
                destination_blob_name=destination_blob_name,
                source_file_bytes=document_bytes,
                content_type=content_type_map.get(file_type, "application/pdf"),
            )
        except se.BucketNotFound:
            main_logger.logger.exception("Bucket not found during upload")
            update_record_with_error(
                data_db, dna_transaction_id, 461, "BUCKET_NOT_EXISTS"
            )
            return 461, "BUCKET_NOT_EXISTS"

        except se.BucketTimeOut:
            main_logger.logger.exception("Bucket timeout during upload")
            update_record_with_error(data_db, dna_transaction_id, 462, "BUCKET_TIMEOUT")
            return 462, "BUCKET_TIMEOUT"

        # * Step 8: Create records in Firestore
        try:
            create_document_record(
                db_client=data_db, dna_transaction_id=dna_transaction_id
            )
            query_ids, queries = create_query_records(
                db_client=data_db,
                dna_transaction_id=dna_transaction_id,
                queries=queries,
            )
            _ = create_page_records(
                db_client=data_db,
                dna_transaction_id=dna_transaction_id,
                page_count=page_count,
            )

        except DocumentQueryResponseTimeout as e:
            main_logger.logger.exception(f"DB timeout creating records: {e}")
            update_record_with_error(data_db, dna_transaction_id, 424, "DB_TIMEOUT")
            return 424, "DB_TIMEOUT"

        # * Step 9: Trigger Workflow
        try:
            workflow_client.trigger_workflow(
                workflow_name=workflow_name,
                dna_transaction_id=dna_transaction_id,
                page_count=page_count,
                queries=queries,
                query_ids=query_ids,
                documents_bucket_folder=documents_bucket_folder,
                pages_bucket_folder=pages_bucket_folder,
                data_bucket_folder=data_bucket_folder,
                bucket_sub_path=bucket_sub_path,
                RequestId=request_id,
                Timestamp=timestamp,
                Version="1.0",
            )
        except WorkflowTimeout as e:
            main_logger.logger.exception(f"Workflow timeout: {e}")
            update_record_with_error(
                data_db, dna_transaction_id, 464, "WORKFLOW_TIMEOUT"
            )
            return 464, "WORKFLOW_TIMEOUT"
        except WorkflowError as e:
            main_logger.logger.exception(f"Workflow error: {e}")
            update_record_with_error(data_db, dna_transaction_id, 465, "WORKFLOW_ERROR")
            return 465, "WORKFLOW_ERROR"

        # Success
        return 200, "OK"
