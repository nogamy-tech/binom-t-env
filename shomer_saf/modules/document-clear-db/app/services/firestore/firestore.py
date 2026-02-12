from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from google.cloud import firestore
from app.services import GCPServiceFactory


class FirestoreClient:
    """
    A client for interacting with a specific Firestore database and collection.
    """

    def __init__(self, gcp_service_factory: GCPServiceFactory, db_name: str, collection_name: Optional[str] = None):
        """
        Initializes the FirestoreClient.

        Args:
            gcp_service_factory (GCPServiceFactory): An instance of the GCPServiceFactory.
            db_name (str): The name of the Firestore database (project ID).
            collection_name (str, optional): The default collection name to use. Defaults to None.
        """
        try:
            self.db = gcp_service_factory.get_gcp_client("firestore", database=db_name)
        except Exception as e:
            raise ValueError(f"Failed to connect to Firestore database '{db_name}': {e}")

        self.db_name = db_name
        self.collection: Optional[firestore.CollectionReference] = None
        self.collection_name: Optional[str] = None
        self.internal_id: Optional[str] = None

        if collection_name:
            self.set_collection(collection_name)

    def set_collection(self, collection_name: str) -> None:
        """
        Sets the collection to be used for subsequent operations.

        Args:
            collection_name (str): The name of the collection.
        """
        self.collection_name = collection_name
        self.collection = self.db.collection(collection_name)

    def set_internal_id(self, internal_id: str) -> None:
        """
        Sets the internal ID for the document to be used for subsequent operations.

        Args:
            internal_id (str): The document ID.
        """
        self.internal_id = internal_id

    def _check_state(self):
        """
        Verifies that the client has a collection and internal_id set.

        Raises:
            ValueError: If collection or internal_id is not set.
        """
        if self.collection is None:
            raise ValueError("Collection not set. Please call set_collection() first.")
        if self.internal_id is None:
            raise ValueError("Internal ID not set. Please call set_internal_id() first.")

    def get_collection(self, collection_name: str) -> firestore.CollectionReference:
        """
        Gets a reference to a specific collection.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            firestore.CollectionReference: A reference to the collection.
        """
        return self.db.collection(collection_name)

    def add_document_to_db(self, **kwargs) -> None:
        """
        Adds or overwrites a document in the current collection.
        The document ID is taken from the currently set `internal_id`.

        Args:
            **kwargs: The fields and values to store in the document.
        """
        self._check_state()
        doc_ref = self.collection.document(self.internal_id)
        doc_ref.set(kwargs)

    def get_document_from_db(self, filter_by: Optional[str] = None, limit: int = 1) -> list[Dict[str, Any]]:
        """
        Retrieves documents from the current collection.

        By default, it retrieves a single document by its ID (using the set `internal_id`).
        If `filter_by` is provided, it queries for documents where a field matches the `internal_id`.

        Args:
            filter_by (str, optional): The field to query against the `internal_id`.
            limit (int, optional): The max number of documents to return when using `filter_by`.

        Returns:
            list[Dict[str, Any]]: A list of dictionary representations of the documents found.
        """
        if self.collection is None:
            raise ValueError("Collection not set. Please call set_collection() first.")

        if filter_by:
            if self.internal_id is None:
                raise ValueError("Internal ID not set for filter value. Please call set_internal_id() first.")

            docs = self.collection.where(field_path=filter_by, op_string="==", value=self.internal_id).limit(limit).stream()
            return [doc.to_dict() for doc in docs]
        else:
            if self.internal_id is None:
                raise ValueError("Internal ID not set. Please call set_internal_id() first.")
            doc_ref = self.collection.document(self.internal_id)
            doc = doc_ref.get()
            return [doc.to_dict()] if doc.exists else []

    def update_document_from_db(self, update_data: Dict[str, Any], filter_by: Optional[str] = None, limit: int = 1) -> None:
        """
        Updates one or more documents in the current collection.

        By default, it updates a single document by its ID (using the set `internal_id`).
        If `filter_by` is provided, it queries and updates documents where a field matches the `internal_id`.

        Args:
            update_data (Dict[str, Any]): A dictionary of fields to update.
            filter_by (str, optional): The field to query against the `internal_id`.
            limit (int): The max number of documents to update when using `filter_by`.
        """
        if self.collection is None:
            raise ValueError("Collection not set. Please call set_collection() first.")

        doc_refs_to_update = []
        if filter_by:
            if self.internal_id is None:
                raise ValueError("Internal ID not set for filter value. Please call set_internal_id() first.")
            docs = self.collection.where(field_path=filter_by, op_string="==", value=self.internal_id).limit(limit).stream()
            doc_refs_to_update = [doc.reference for doc in docs]
        else:
            if self.internal_id is None:
                raise ValueError("Internal ID not set. Please call set_internal_id() first.")
            doc_refs_to_update.append(self.collection.document(self.internal_id))

        if not doc_refs_to_update:
            print("No document found to update.")
            return

        for doc_ref in doc_refs_to_update:
            doc_ref.update(update_data)

    def _delete_doc_ref(self, doc_ref: firestore.DocumentReference, time_cutoff: int) -> bool:
        """
        Internal helper to delete a single document reference with a time cutoff check.

        Args:
            doc_ref (firestore.DocumentReference): The document reference to delete.
            time_cutoff (int): If > 0, only deletes if the 'date' field is older than this many hours.

        Returns:
            bool: True if the document was deleted, False otherwise.
        """
        doc_to_delete = doc_ref.get()
        if not doc_to_delete.exists:
            return False

        can_delete = True
        if time_cutoff > 0:
            doc_data = doc_to_delete.to_dict()
            doc_date = doc_data.get("date")
            if doc_date:
                now = datetime.now()
                cutoff_datetime = now - timedelta(hours=time_cutoff)

                if doc_date > cutoff_datetime:
                    can_delete = False
                    print(f"Document {doc_to_delete.id} is not older than {time_cutoff} hours. Skipping deletion.")
            else:
                can_delete = False
                print(f"Document {doc_to_delete.id} has no 'date' field. Skipping deletion due to time_cutoff.")

        if can_delete:
            doc_id = doc_ref.id
            doc_ref.delete()
            print(f"Document with id '{doc_id}' has been deleted from '{self.collection_name}'.")
            return True

        return False

    def delete_document_from_db(self, filter_by: Optional[str] = None, time_cutoff: int = 0, limit: int = 1) -> None:
        """
        Deletes documents from the current collection one by one.

        Note: This method performs individual delete operations. For deleting multiple
        documents, `delete_batch_from_db` is significantly more efficient.

        By default, it deletes a single document by its ID (using the set `internal_id`).
        If `filter_by` is provided, it queries and deletes documents where a field matches the `internal_id`.

        Args:
            filter_by (str, optional): The field to query against the `internal_id`.
            time_cutoff (int): If > 0, only deletes if the 'date' field is older than this many hours.
            limit (int): The max number of documents to delete when using `filter_by`.
        """
        if self.collection is None:
            raise ValueError("Collection not set. Please call set_collection() first.")

        doc_refs_to_delete = []
        if filter_by:
            if self.internal_id is None:
                raise ValueError("Internal ID not set for filter value. Please call set_internal_id() first.")
            docs = self.collection.where(field_path=filter_by, op_string="==", value=self.internal_id).limit(limit).stream()
            doc_refs_to_delete.extend(doc.reference for doc in docs)
        else:
            if self.internal_id is None:
                raise ValueError("Internal ID not set. Please call set_internal_id() first.")
            doc_refs_to_delete.append(self.collection.document(self.internal_id))

        deleted_count = 0
        if not doc_refs_to_delete:
            print("No document found to delete.")
            return

        for doc_ref in doc_refs_to_delete:
            if self._delete_doc_ref(doc_ref, time_cutoff):
                deleted_count += 1

        if deleted_count == 0 and doc_refs_to_delete:
            print("All documents found were skipped and not deleted.")
        elif deleted_count > 0:
            print(f"Successfully deleted {deleted_count} document(s).")

    def delete_batch_from_db(self, filter_by: str, batch_size: int = 500) -> int:
        """
        Deletes all documents matching a filter criterion using efficient batches.

        This is the recommended method for deleting multiple documents. It queries for
        all documents where the `filter_by` field matches the currently set `internal_id`.

        Args:
            filter_by (str): The field to query against the `internal_id`.
            batch_size (int): The number of documents per batch. Max and default is 500.

        Returns:
            int: The total number of documents deleted.
        """
        if self.collection is None:
            raise ValueError("Collection not set. Please call set_collection() first.")
        if self.internal_id is None:
            raise ValueError("Internal ID not set for filter value. Please call set_internal_id() first.")

        query = self.collection.where(field_path=filter_by, op_string="==", value=self.internal_id)
        total_deleted = 0

        # Firestore cursors are stateful, so we process in a loop until no documents are left
        while True:
            docs = query.limit(batch_size).stream()

            # It's more efficient to check if the first document exists than to count them all
            try:
                first_doc = next(docs)
            except StopIteration:
                break  # No more documents to delete

            batch = self.db.batch()

            # Add the first document to the batch
            batch.delete(first_doc.reference)
            num_in_batch = 1

            # Add the rest of the documents from the stream to the batch
            for doc in docs:
                batch.delete(doc.reference)
                num_in_batch += 1

            batch.commit()
            total_deleted += num_in_batch
            print(f"Committed a batch of {num_in_batch} deletes for DnaTransactionId '{self.internal_id}'.")

        if total_deleted > 0:
            print(f"Successfully deleted a total of {total_deleted} documents.")
        else:
            print("No documents found to delete for the given filter.")

        return total_deleted

    def write_llm_answer_to_db(
        self,
        DnaTransactionId: str,
        Page_number: int,
        Query_number: int,
        Query: str,
        QueryResponse: Dict[str, Any],
        RequestErrorMessage: str,
        RequestErrorCode: str,
        status: str,
        date: datetime,
    ) -> str:
        """Writes a new document containing an LLM answer to the database.

        Note: The caller is responsible for calling `set_internal_id()` with the
        desired document ID before invoking this method.

        Args:
            DnaTransactionId (str): The transaction ID.
            Page_number (int): The page number related to the query.
            Query_number (int): The query number.
            Query (str): The query text.
            QueryResponse (Dict[str, Any]): The response from the LLM.
            RequestErrorMessage (str): Any error message.
            RequestErrorCode (str): Any error code.
            status (str): The status of the operation.
            date (datetime): The timestamp of the operation.
        """
        self._check_state()
        try:
            self.add_document_to_db(
                DnaTransactionId=DnaTransactionId,
                Page_number=Page_number,
                Query_number=Query_number,
                Query=Query,
                QueryResponse=QueryResponse,
                RequestErrorMessage=RequestErrorMessage,
                RequestErrorCode=RequestErrorCode,
                status=status,
                date=date,
            )
            return "SUCCESS"
        except Exception:
            return "ERROR"

    def print_collection(self) -> None:
        """
        Prints all documents in the currently set collection.
        """
        if self.collection is None:
            raise ValueError("Collection not set. Please call set_collection() first.")

        docs = self.collection.stream()

        for doc in docs:
            print(f"{doc.id} => {doc.to_dict()}")

    def clean_collection(self, time_cutoff: int = 0, batch_size: int = 500) -> None:
        """
        Deletes documents from the entire collection, one by one.

        Warning: This method iterates through the collection and issues a separate
        delete for each document, which can be slow and costly for large collections.
        It fetches documents in batches but does not use batched writes.
        The process is recursive to handle collections larger than the batch size.

        Args:
            time_cutoff (int): If > 0, only deletes documents with a 'date' field older than this many hours.
            batch_size (int): The number of documents to fetch and delete in each recursive step.
        """
        if self.collection is None:
            raise ValueError("Collection not set. Please call set_collection() first.")

        query = self.collection
        if time_cutoff > 0:
            local_now = datetime.now()
            cutoff_local = local_now - timedelta(hours=time_cutoff)

            print(f"Cleaning documents older than {cutoff_local.isoformat()} (local time)")
            query = query.where(field_path="date", op_string="<=", value=cutoff_local)

        docs = query.limit(batch_size).stream()
        deleted = 0

        for doc in docs:
            print(f"Deleting {doc.id}")
            doc.reference.delete()
            deleted += 1

        if deleted >= batch_size:
            # Recurse
            return self.clean_collection(time_cutoff=time_cutoff, batch_size=batch_size)
