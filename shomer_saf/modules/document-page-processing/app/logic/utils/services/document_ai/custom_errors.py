

class DocumentNotFound(Exception):
    """Custom alert for when the document is missing."""
    pass


class DocumentAITimeout(Exception):
    """Custom alert for when the document is timed out."""
    pass

class DocumentAIFailure(Exception):
    """Custom alert for when the document is failed."""
    pass

class ImgQualityInvalid(Exception):
    """Custom alert for when the image quality is invalid."""
    pass


