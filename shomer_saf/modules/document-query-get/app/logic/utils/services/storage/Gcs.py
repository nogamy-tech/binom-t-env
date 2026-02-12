from typing import Tuple
import mimetypes
import os
from io import BytesIO

# modules
from .custom_errors import BucketNotFound, BucketTimeOut, MultipleFilesFound, BlobNotFound

# handling errors
from google.api_core.exceptions import NotFound, DeadlineExceeded, ServiceUnavailable, Forbidden

import socket
from app.logic.utils.services import GCPServiceFactory


class Gcs:
    def __init__(self, gcp_service_factory: GCPServiceFactory, bucket_name: str, timeout: int = 600):
        """
        Initializes the GCS client and connects to a specific bucket.

        This constructor uses a GCPServiceFactory to get a storage client and then
        retrieves the specified bucket. It sets a timeout for the connection attempt.

        Args:
            gcp_service_factory (GCPServiceFactory): Factory for creating GCP clients.
            bucket_name (str): Name of the GCS bucket to connect to.
            timeout (int, optional): Request timeout in seconds. Defaults to 600.

        Raises:
            BucketNotFound: If the bucket does not exist, access is denied, or the
                            service is unavailable.
            BucketTimeOut: If the connection request times out.
        """
        try:
            self.client = gcp_service_factory.get_gcp_client("storage")
            self.bucket = self.client.get_bucket(bucket_name, timeout=timeout)
            self.bucket_name = bucket_name
        except NotFound:
            raise BucketNotFound(f"❌ Bucket '{bucket_name}' not found.")
        except Forbidden:
            raise BucketNotFound(f"🚫 Access denied to bucket '{bucket_name}'. Check permissions.")
        except ServiceUnavailable:
            raise BucketNotFound(f"🚫 GCS service is unavailable for bucket '{bucket_name}'.")
        except DeadlineExceeded:
            raise BucketTimeOut(f"⏱️ Request to GCS timed out for bucket '{bucket_name}'.")
        except socket.timeout:
            raise BucketTimeOut(f"⏱️ Socket timeout while accessing bucket '{bucket_name}'.")

    def process_blob_from_gcs(self, sub_folder: str, blob_name: str) -> Tuple[bytes, str]:
        """
        Downloads a single blob from a Google Cloud Storage subfolder.

        Ensures the subfolder contains exactly one file. Returns the blob's
        content as bytes and its MIME type.

        Args:
            sub_folder: Subfolder (prefix) within the bucket.
            blob_name: Name of the blob to retrieve.

        Returns:
            Tuple[bytes, str]: The blob's content and its content type.

        Raises:
            MultipleFilesFound: If more than one file exists in the subfolder.
            BlobNotFound: If the specified blob is not found in the bucket.
        """
        full_blob_name = f"{sub_folder}/{blob_name}"

        if self.count_blobs_in_subfolder(subfolder_prefix=sub_folder) > 1:
            raise MultipleFilesFound(f"inside {self.bucket_name}/{sub_folder} there is more than one file in the bucket")

        try:
            blob = self.bucket.blob(full_blob_name)
            file_bytes = blob.download_as_bytes()
        except NotFound:
            raise BlobNotFound(f"📁 Blob '{blob_name}' not found in bucket '{self.bucket_name}/{sub_folder}'.")

        file_type = blob.content_type
        return file_bytes, file_type

    def upload_to_gcs(
        self,
        destination_blob_name: str,
        source_file_path: str = None,
        source_file_bytes: bytes = None,
        source_file_text: str = None,
        content_type: str = None,
    ) -> None:
        """
        Uploads a file to a Google Cloud Storage bucket from a local file path, bytes, or text.

        Args:
            destination_blob_name (str): Destination path and filename in the bucket.
            source_file_path (str, optional): Local file path to upload.
            source_file_bytes (bytes, optional): File content in bytes to upload.
            source_file_text (str, optional): File content as a text string to upload.
            content_type (str, optional): MIME type of the uploaded file.

        Raises:
            FileNotFoundError: If `source_file_path` does not exist.
            ValueError: If multiple source formats are provided or no source is given.
        """
        blob = self.bucket.blob(destination_blob_name)

        if blob.exists():
            print(f"The file 'gs://{self.bucket_name}/{destination_blob_name}' already exists in the bucket.")
            print("Rewriting the file")

        if sum(bool(x) for x in [source_file_path, source_file_bytes, source_file_text]) > 1:
            raise ValueError("The file's content can only be provided in a single format")

        if source_file_path:
            if not os.path.exists(source_file_path):
                raise FileNotFoundError(f"The file '{source_file_path}' does not exist")
            blob.upload_from_filename(source_file_path, content_type=content_type)
        elif source_file_bytes:
            tiff_io = BytesIO(source_file_bytes)
            blob.upload_from_file(tiff_io, content_type=content_type or "image/tiff")
        elif source_file_text:
            blob.upload_from_string(source_file_text, content_type=content_type or "text/markdown")
        else:
            raise ValueError("No file was provided to upload")

        print(f"File uploaded to 'gs://{self.bucket_name}/{destination_blob_name}'.")

    def read_gcs_file(self, blob_name: str) -> bytes | str:
        """
        Reads a file from Google Cloud Storage.

        Args:
            blob_name (str): Name of the blob (file) in the bucket.

        Returns:
            str or bytes: File contents (text or binary).

        Raises:
            BlobNotFound: If the specified blob does not exist in the bucket.
        """
        blob = self.bucket.blob(blob_name)

        if not blob.exists():
            raise BlobNotFound(f"📁 Blob '{blob_name}' not found in bucket '{self.bucket_name}/{blob_name}'.")

        mime_type, _ = mimetypes.guess_type(blob_name)

        if mime_type and mime_type.startswith("text"):
            return blob.download_as_text()
        else:
            return blob.download_as_bytes()

    def get_blob_name(self, internal_id: str) -> str:
        """
        Searches for a blob in the GCS bucket whose name contains the given internal_id.

        Args:
            internal_id (str): The identifier to search for in blob names.

        Returns:
            str: The name of the first blob that matches the internal_id.

        Raises:
            FileNotFoundError: If no matching blob is found.
        """
        matching_blobs = [blob.name for blob in self.bucket.list_blobs() if internal_id in blob.name.strip("/")]

        if not matching_blobs:
            raise FileNotFoundError(f"No blob found in bucket '{self.bucket_name}' with internal ID '{internal_id}'.")

        return matching_blobs[0]

    def delete_blob(self, blob_name: str) -> None:
        """
        Deletes a blob (file) from a Google Cloud Storage bucket.

        Args:
            blob_name (str): Name of the blob (file) to delete.
        """
        try:
            blob = self.bucket.blob(blob_name)
            blob.delete()
            print(f"✅ Blob '{blob_name}' deleted from bucket '{self.bucket_name}'.")
        except Exception as e:
            print(f"❌ Failed to delete blob '{blob_name}': {e}")

    def count_blobs_in_subfolder(self, subfolder_prefix: str) -> int:
        """
        Count the number of blobs inside a "subfolder" in a GCS bucket.

        Args:
            subfolder_prefix (str): The prefix of the subfolder (e.g., "folder1/subfolder1/").

        Returns:
            int: Number of blobs inside the subfolder.
        """
        blobs = list(self.bucket.list_blobs(prefix=subfolder_prefix))
        return len(blobs)

    def print_blobs_in_subfolder(self, subfolder_prefix: str) -> None:
        """
        Print the names of all blobs within a specified subfolder of a GCS bucket.

        Args:
            subfolder_prefix (str): The prefix representing the subfolder path.
        """
        for blob in self.bucket.list_blobs(prefix=subfolder_prefix):
            print(blob.name)


if __name__ == "__main__":
    # Example usage:
    # Replace 'your-bucket-name' with your actual bucket name
    try:
        factory = GCPServiceFactory()
        gcs_service = Gcs(gcp_service_factory=factory, bucket_name="bucket_shomer_saf-940c4fa147fe6a40")
        print(f"Successfully connected to bucket: {gcs_service.bucket.name}")

        # Example: list blobs in a subfolder
        # gcs_service.print_blobs_in_subfolder(subfolder_prefix="your-subfolder/")

    except (BucketNotFound, BucketTimeOut) as e:
        print(e)
