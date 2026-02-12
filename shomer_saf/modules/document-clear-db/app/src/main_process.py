from app.config import load_config
from app.services import Gcs, custom_errors as se
from app.services import FirestoreClient


from app.services import GCPServiceFactory


def clear_db_process(gcp_service_factory: GCPServiceFactory, transactions: list[str]) -> tuple[int, str]:
    """
    Clear specified transactions from both cloud storage buckets and Firestore.

    If `transactions` is empty, all content in the predefined buckets and database is cleared.
    Handles errors related to bucket access, blob existence, and database failures.

    Args:
        gcp_service_factory (GCPServiceFactory): An instance of the GCPServiceFactory.
        transactions (list[str]): List of transaction IDs to clear. If empty, clears everything.

    Returns:
        tuple[int, str]: Status code and message indicating the result of the operation.
            Common codes include:
                200: SUCCESS
                461: BUCKET_NOT_EXISTS
                463: NO_DOCUMENT_IN_BUCKET
                500: BUCKET_TIMEOUT or DB_FAILURE
    """
    config = load_config()

    if transactions:
        print(f"the transaction to delete that were given are: {transactions}")

    else:
        print("no transaction were given. clearing db and buckets")

    try:
        bucket_client = Gcs(gcp_service_factory=gcp_service_factory, bucket_name=config["project"]["bucket"])
        clear_buckets(bucket_client, transactions)

    except se.BucketNotFound:
        RequestErrorCode, RequestErrorMessage = 461, "BUCKET_NOT_EXISTS"
        return RequestErrorCode, RequestErrorMessage

    except se.BucketTimeOut:
        RequestErrorCode, RequestErrorMessage = 500, "BUCKET_TIMEOUT"
        return RequestErrorCode, RequestErrorMessage

    except se.BlobNotFound:
        RequestErrorCode, RequestErrorMessage = 463, "NO_DOCUMENT_IN_BUCKET"
        return RequestErrorCode, RequestErrorMessage

    try:
        firestore_client = FirestoreClient(gcp_service_factory=gcp_service_factory, db_name=config["project"]["db_name"], collection_name=config["project"]["collection_name"])
        clear_firestore(firestore_client, transactions)

    except Exception:
        RequestErrorCode, RequestErrorMessage = 500, "DB_FAILURE"
        return RequestErrorCode, RequestErrorMessage

    RequestErrorCode, RequestErrorMessage = 200, "SUCCESS"
    return RequestErrorCode, RequestErrorMessage


def clear_buckets(bucket_client: Gcs, transactions: list[str]) -> None:
    """
    Clear specified cloud storage buckets by deleting blobs or folders.

    If `transactions` is empty, all content in predefined project buckets is deleted.
    Otherwise, only blobs matching the transaction IDs are deleted.

    Args:
        bucket_client (Gcs): The GCS client to use for bucket operations.
        transactions (list[str]): List of transaction IDs to clear. If empty, all content is deleted.

    Returns:
        None.
    """
    config = load_config()

    main_bucket = config["project"]["bucket"]
    folders = [
        config["project"]["documents_bucket"],
        config["project"]["pages_bucket"],
        config["project"]["data_bucket"],
    ]

    if not transactions:
        for folder in folders:
            # if no transaction were given - delete all buckets' content
            print(f"clearing the bucket {main_bucket}/{folder}")
            bucket_client.delete_folder(folder_name=folder, time_cutoff=config["project"]["time_to_clear_buckets"])
        else:
            for transaction in transactions:
                # find a blob in the bucket that containes the name of the transaction (even if its a folder)
                blobs = bucket_client.get_blobs(internal_id=transaction)
                for blob in blobs:
                    bucket_client.delete_blob(blob_name=blob)

    print("finished clearing buckets")


def clear_firestore(firestore_client: FirestoreClient, transactions: list[str]) -> None:
    """
    Clear documents from Firestore based on provided transaction IDs.

    If `transactions` is empty, all documents older than a configured time cutoff are deleted
    from the project's collection.

    Args:
        firestore_client (FirestoreClient): The Firestore client for database operations.
        transactions (list[str]): List of transaction IDs to delete. If empty, clears old documents.

    Returns:
        None
    """
    config = load_config()

    if transactions:
        for transaction in transactions:
            firestore_client.set_internal_id(transaction)
            firestore_client.delete_document_from_db(filter_by="DnaTransactionId", limit=1000)

    else:
        firestore_client.clean_collection(time_cutoff=config["project"]["time_to_clear_firestore"])

    print("finished clearing DB")
