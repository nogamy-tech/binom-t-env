"""
Main processing logic for Document Query Get.
"""

from typing import Dict, Tuple, List, Optional
from .utils.config import create_config_file, load_config
from .utils.services import GCPServiceFactory
from .utils.services.firestore import FirestoreClient
from .utils.src.accounts_db import query_accounts_db, AccountsDBTimeout, UnknownClient
from .utils.src.logging import log_to_cloud_logging
from .utils.src.documents_query_jobs import query_documents_query_jobs, DocumentsQueryJobsTimeout, DnaTransactionIdNotFound
from .utils.src.aggregations import aggregate_query_responses
from .utils.src.documents_query_jobs import update_record_with_error
from app.logic.utils.services.logging import ExecutionLogger

main_logger = ExecutionLogger(customer_id="document-query-get")

class DocumentQueryGetProcess:
    """
    Main processing class for Document Query Get.
    """

    @staticmethod
    def run_process(msg: Dict) -> Tuple[int, str, Optional[List[Dict]], Optional[List[Dict]], Optional[Dict]]:
        """
        Process a document query get request.

        Args:
            msg: Dictionary containing request data with:
                - ClientRequestId: str
                - x_client_id: str
                - x_client_secret: str (optional)
                - x_scope: str

        Returns:
            tuple[int, str, Optional[List[Dict]], Optional[List[Dict]], Optional[Dict]]:
            (error_code, message, queries_page_results, queries_results, queries_aggregated_results)
        """
        return DocumentQueryGetProcess.main_process(
            client_request_id=msg.get("ClientRequestId"), x_client_id=msg.get("x_client_id"), x_client_secret=msg.get("x_client_secret"), x_scope=msg.get("x_scope")
        )

    @staticmethod
    @main_logger.log_execution
    def main_process(client_request_id: str, x_client_id: str, x_client_secret: str, x_scope: str) -> Tuple[int, str, Optional[List[Dict]], Optional[List[Dict]], Optional[Dict]]:
        """
        Main processing logic for Document Query Get.

        Returns:
            Tuple[int, str, Optional[List[Dict]], Optional[List[Dict]], Optional[Dict]]:
            (error_code, error_message, queries_page_results, queries_results, queries_aggregated_results)
        """
        
        main_logger.logger.info("Start document-query-get")
        gcp_service_factory = GCPServiceFactory()
        create_config_file(gcp_service_factory=gcp_service_factory)
        config = load_config()

        # define service clients
        data_db = FirestoreClient(gcp_service_factory=gcp_service_factory, db_name=config["project"]["db_name"], collection_name=config["project"]["collection_name"])
        accounts_db = FirestoreClient(gcp_service_factory=gcp_service_factory, db_name=config["project"]["accounts_db"], collection_name=config["project"]["accounts_collection"])

        # * Step 1: Query AccountsDB
        try:
            data = query_accounts_db(db_client=accounts_db, x_client_id=x_client_id, x_scope=x_scope)
            ministry_name = data.get("MinistryName")
            project_name = data.get("ProjectName")

        except AccountsDBTimeout as e:
            main_logger.logger.exception(f"AccountsDB timeout: {e}")
            update_record_with_error(data_db, client_request_id, 500, "ACCOUNTS_DB_TIMEOUT")
            return 500, "ACCOUNTS_DB_TIMEOUT", None, None, None

        except UnknownClient as e:
            main_logger.logger.exception(f"Unknown client: {e}")
            update_record_with_error(data_db, client_request_id, 500, "UNKNOWN_CLIENT")
            return 500, "UNKNOWN_CLIENT", None, None, None

        # Step 3: Generate DnaTransactionId
        dna_transaction_id = f"{ministry_name}_{project_name}_{client_request_id}"

        ministry_name, project_name, client_request_id = dna_transaction_id.split("_")
        main_logger.set_context(customer_id=client_request_id,ministry_name=ministry_name,project_name=project_name,dna_transaction_id=dna_transaction_id)


        # dna_transaction_id = client_request_id
        main_logger.logger.info("Generated DnaTransactionId")

        # Step 4: Query DocumentsQueryJobs
        try:
            query_docs = query_documents_query_jobs(db_client=data_db,dna_transaction_id=dna_transaction_id)
        except DocumentsQueryJobsTimeout as e:
            main_logger.logger.exception(f"DocumentsQueryJobs timeout: {e}")
            update_record_with_error(data_db,dna_transaction_id, 500, "DB_TIMEOUT")
            return 500, "DB_TIMEOUT", None, None, None

        except DnaTransactionIdNotFound as e:
            main_logger.logger.exception(f"DnaTransactionId not found: {e}")
            update_record_with_error(data_db,dna_transaction_id, 500, "NO_CONTENT")
            return 500, "NO_CONTENT", None, None, None

        # Step 5: Aggregate query responses
        try:
            queries_page_results, queries_results, queries_aggregated_results = aggregate_query_responses(query_docs)
            main_logger.logger.info("Aggregated query responses")

            # Step 6: Return response
            if queries_results:
                return 200, "OK", queries_page_results, queries_results, queries_aggregated_results
            else:
                main_logger.logger.exception("No queries found in results")
                return 500, "INTERNAL_ERROR", None, None, None

        except Exception as e:
            main_logger.logger.exception(f"Error aggregating query responses: {e}")
            update_record_with_error(data_db,dna_transaction_id, 500, "INTERNAL_ERROR")
            return 500, "INTERNAL_ERROR", None, None, None
