from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from google.cloud import firestore
from app.logic.utils.services import GCPServiceFactory


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
        Adds a document to the collection in the Firestore database.
        Assumes collection and internal_id are already set.

        Args:
            **kwargs: Additional fields to store in the document.
        """
        self._check_state()
        doc_ref = self.collection.document(self.internal_id)
        doc_ref.set(kwargs)

    def get_document_from_db(self, filter_by: Optional[str] = None, limit: int = 1) -> list[Dict[str, Any]]:
        """
        Retrieves documents from a collection in Firestore.
        Can get by document ID (default) or by filtering on a field matching the internal_id.

        Args:
            filter_by (str, optional): If provided, this field name will be used to query for a
                                       document where the field value equals the currently set internal_id.
                                       If not provided, the document is retrieved by its ID.
            limit (int, optional): The maximum number of documents to return when filtering. Defaults to 1.

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

    def update_document_from_db(self, key: str, value: Any, filter_by: Optional[str] = None, limit: int = 1) -> None:
        """
        Updates a specific field in a Firestore document.
        Can find the document by ID (default) or by filtering on a field.

        Args:
            key (str): The field name to update.
            value (Any): The new value to assign to the field.
            filter_by (str, optional): If provided, finds the document to update by querying
                                       where this field equals the set internal_id.
            limit (int): The number of documents to update. Defaults to 1.
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
            doc_ref.update({key: value})

    def _delete_doc_ref(self, doc_ref: firestore.DocumentReference, time_cutoff: int) -> bool:
        """Helper to delete a document with a time cutoff check."""
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
        Deletes documents from a collection in Firestore.
        Can find the document by ID (default) or by filtering on a field.
        An optional time cutoff can prevent deletion of recent documents.

        Args:
            filter_by (str, optional): If provided, finds documents to delete by querying
                                       where this field equals the set internal_id.
            time_cutoff (int, optional): If greater than 0, specifies a cutoff in hours.
                                         Only documents with a 'date' field older than this
                                         cutoff will be deleted. Defaults to 0 (no time check).
            limit (int): The number of documents to delete when filtering. Defaults to 1.
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
        """
        Writes an LLM answer to the database.
        Assumes collection and internal_id are already set.
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
        Recursively deletes documents in the currently set collection, in batches.
        An optional time cutoff can preserve recent documents.

        Args:
            time_cutoff (int, optional): If greater than 0, specifies a cutoff in hours.
                                         Only documents with a 'date' field older than this
                                         cutoff will be deleted. Defaults to 0 (delete all).
            batch_size (int, optional): The number of documents to delete in each batch.
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
