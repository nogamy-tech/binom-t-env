"""
Utilities for querying DocumentsQueryJobs (Firestore) to get query responses.
"""

from typing import List, Dict
from google.api_core.exceptions import DeadlineExceeded, NotFound
from app.logic.utils.services import FirestoreClient


class DocumentsQueryJobsTimeout(Exception):
    """Raised when DocumentsQueryJobs query times out"""

    pass


class DnaTransactionIdNotFound(Exception):
    """Raised when DnaTransactionId not found in DocumentsQueryJobs"""

    pass


def query_documents_query_jobs(db_client: FirestoreClient, dna_transaction_id: str) -> List[Dict]:
    """
    Queries DocumentsQueryJobs to retrieve all query responses for a given DnaTransactionId.

    This function searches the 'DocumentsQueryJobs' collection for all documents
    that match the provided `dna_transaction_id`. It's designed to fetch all
    related job documents for a single transaction.

    Args:
        db_client: An instance of the Firestore client.
        dna_transaction_id: The transaction ID to query for.

    Returns:
        A list of dictionaries, where each dictionary is a document from Firestore.

    Raises:
        DocumentsQueryJobsTimeout: If the database query exceeds the time limit.
        DnaTransactionIdNotFound: If no documents are found for the given `dna_transaction_id`.
    """
    db_client.set_internal_id(dna_transaction_id)
    results=[]
    try:
        docs = db_client.get_document_from_db(filter_by="DnaTransactionId", limit=1000)

        for doc in docs:
            if "QueryResponse" in doc:
                results.append(doc)
                
        if not results:
            raise DnaTransactionIdNotFound(f"DnaTransactionId '{dna_transaction_id}' not found in DocumentsQueryJobs")

        return results

    except DeadlineExceeded:
        raise DocumentsQueryJobsTimeout(f"DocumentsQueryJobs query timed out for {dna_transaction_id}")
    except NotFound:
        raise DnaTransactionIdNotFound(f"DnaTransactionId '{dna_transaction_id}' not found in DocumentsQueryJobs")

    except DocumentsQueryJobsTimeout:
        raise
    except DnaTransactionIdNotFound:
        raise
    except Exception as e:
        # For any other error, treat as timeout for now
        if "deadline" in str(e).lower() or "timeout" in str(e).lower():
            raise DocumentsQueryJobsTimeout(f"DocumentsQueryJobs query timed out: {e}")
        raise DnaTransactionIdNotFound(f"Error querying DocumentsQueryJobs: {e}")


def update_record_with_error(db_client: FirestoreClient, dna_transaction_id: str, error_code: int, error_message: str) -> None:
    """
    Updates all records for a given transaction with an error status and message.

    This function finds all documents in the 'DocumentsQueryJobs' collection where
    the 'DnaTransactionId' field matches the provided ID. It then updates these
    documents to set an error status, code, and message. This is typically used
    to mark a failed transaction across all its related jobs.

    Args:
        db_client: An instance of the Firestore client.
        dna_transaction_id: The transaction ID to update records for.
        error_code: The error code to set.
        error_message: The error message to set.

    Raises:
        DocumentsQueryJobsTimeout: If the database update operation times out.
    """
    db_client.set_internal_id(dna_transaction_id)
    try:
        update_data = {
            "status": "Ended_DocumentProcessQuery",
            "RequestErrorCode": error_code,
            "RequestErrorMessage": error_message,
        }
        db_client.update_document_from_db(update_data=update_data, filter_by="DnaTransactionId", limit=1000)

    except DeadlineExceeded:
        raise DocumentsQueryJobsTimeout(f"Timeout updating error record for {dna_transaction_id}")
    except Exception as e:
        if "deadline" in str(e).lower() or "timeout" in str(e).lower():
            raise DocumentsQueryJobsTimeout(f"Timeout updating error record: {e}")
        # Don't raise for update errors - log them instead
        print(f"Warning: Failed to update error record: {e}")
