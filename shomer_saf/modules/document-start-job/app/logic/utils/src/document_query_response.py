"""
Utilities for managing DocumentQueryResponse records in Firestore.
"""

from typing import List, Dict
from google.api_core.exceptions import DeadlineExceeded
from app.logic.utils.services import FirestoreClient
from datetime import datetime
from copy import deepcopy

class DocumentQueryResponseTimeout(Exception):
    """Raised when DocumentQueryResponse operations timeout"""

    pass


def create_document_record(db_client: FirestoreClient, dna_transaction_id: str) -> None:
    """
    Creates a single document record representing the overall job status.

    Args:
        db_client: The Firestore client.
        dna_transaction_id: The unique ID for the transaction, used as the document ID.

    Raises:
        DocumentQueryResponseTimeout: If the operation times out
    """
    db_client.set_internal_id(dna_transaction_id)
    try:
        db_client.add_document_to_db(DnaTransactionId=dna_transaction_id, status="Pending", Type="Document",  date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    except DeadlineExceeded:
        raise DocumentQueryResponseTimeout(f"Timeout creating document record for {dna_transaction_id}")
    except Exception as e:
        if "deadline" in str(e).lower() or "timeout" in str(e).lower():
            raise DocumentQueryResponseTimeout(f"Timeout creating document record: {e}")
        raise


def create_query_records(db_client: FirestoreClient, dna_transaction_id: str, queries: List[Dict[str, str]]) -> List[str]:
    """
    Creates a Firestore document for each query with a "Pending" status.

    Args:
        db_client: The Firestore client.
        dna_transaction_id: The base ID for the transaction.
        queries: A list of query dictionaries, each with "query" and "model" keys.

    Returns:
        A list of the generated document IDs for each query record.
        A list of updated queries (with id numbers)

    Raises:
        DocumentQueryResponseTimeout: If the operation times out
    """
    new_queries=deepcopy(queries)
    
    try:
        query_ids = []

        for idx, query_item in enumerate(new_queries):
            query_id = f"{dna_transaction_id}_Query_{idx}"
            db_client.set_internal_id(query_id)
            query_ids.append(query_id)
            query_item["id"]=str(idx)
            db_client.add_document_to_db(DnaTransactionId=dna_transaction_id, status="Pending", Type="Query", Order=idx, Query=query_item.get("query"), Model=query_item.get("model"), date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return query_ids,new_queries

    except DeadlineExceeded:
        raise DocumentQueryResponseTimeout(f"Timeout creating query records for {dna_transaction_id}")
    except Exception as e:
        if "deadline" in str(e).lower() or "timeout" in str(e).lower():
            raise DocumentQueryResponseTimeout(f"Timeout creating query records: {e}")
        raise


def create_page_records(db_client: FirestoreClient, dna_transaction_id: str, page_count: int) -> List[str]:
    """
    Creates a Firestore document for each page with a "Pending" status.

    Args:
        db_client: The Firestore client.
        dna_transaction_id: The base ID for the transaction.
        page_count: The total number of pages to create records for.

    Returns:
        A list of the generated document IDs for each page record.

    Raises:
        DocumentQueryResponseTimeout: If the operation times out
    """

    try:
        page_ids = []

        for page_num in range(page_count):
            page_id = f"{dna_transaction_id}_Page_{page_num}"
            db_client.set_internal_id(page_id)
            page_ids.append(page_id)

            db_client.add_document_to_db(DnaTransactionId=dna_transaction_id, status="Pending", Type="Page", Order=page_num, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return page_ids

    except DeadlineExceeded:
        raise DocumentQueryResponseTimeout(f"Timeout creating page records for {dna_transaction_id}")
    except Exception as e:
        if "deadline" in str(e).lower() or "timeout" in str(e).lower():
            raise DocumentQueryResponseTimeout(f"Timeout creating page records: {e}")
        raise


def delete_existing_records(db_client: FirestoreClient, dna_transaction_id: str) -> None:
    """
    Deletes all existing records for a given DnaTransactionId using a batch operation.

    Args:
        db_client: The Firestore client.
        dna_transaction_id: The transaction ID to filter and delete records by.

    Raises:
        DocumentQueryResponseTimeout: If the operation times out
    """
    db_client.set_internal_id(dna_transaction_id)
    try:
        db_client.delete_batch_from_db(
            filter_by="DnaTransactionId",
        )

    except DeadlineExceeded:
        raise DocumentQueryResponseTimeout(f"Timeout deleting existing records for {dna_transaction_id}")
    except Exception as e:
        if "deadline" in str(e).lower() or "timeout" in str(e).lower():
            raise DocumentQueryResponseTimeout(f"Timeout deleting existing records: {e}")
        raise


def update_record_with_error(db_client: FirestoreClient, dna_transaction_id: str, error_code: int, error_message: str) -> None:
    """
    Updates all records for a transaction with an error status and message.

    This function finds all documents where 'DnaTransactionId' matches the given
    ID and updates them to reflect an error state. It logs but does not re-raise
    exceptions to prevent process termination on logging failures.

    Args:
        db_client: The Firestore client.
        dna_transaction_id: The transaction ID to update records for.
        error_code: The error code to set.
        error_message: The error message to set.
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
        raise DocumentQueryResponseTimeout(f"Timeout updating error record for {dna_transaction_id}")
    except Exception as e:
        if "deadline" in str(e).lower() or "timeout" in str(e).lower():
            raise DocumentQueryResponseTimeout(f"Timeout updating error record: {e}")
        # Don't raise for update errors - log them instead
        print(f"Warning: Failed to update error record: {e}")
