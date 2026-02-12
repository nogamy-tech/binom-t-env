class BucketNotFound(Exception):
    """Custom alert for when the GCS bucket is missing."""

    pass


class BucketTimeOut(Exception):
    """Custom alert for when the GCS bucket is Timed Out."""

    pass


class MultipleFilesFound(Exception):
    """Custom alert for when the number of documents inside a blob is more than 1"""

    pass


class BlobNotFound(Exception):
    """Custom alert for when the blob is missing."""

    pass
