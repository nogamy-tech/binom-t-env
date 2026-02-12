"""
Utilities for validating document format and integrity.
"""

import base64
import io
from typing import Tuple
from PIL import Image
import fitz  # PyMuPDF


class UnsupportedFormat(Exception):
    """Raised when document format is not supported"""

    pass


class UnreadableFile(Exception):
    """Raised when document is corrupted or encrypted"""

    pass


def _validate_pdf(document_bytes: bytes) -> Tuple[str, int]:
    """Validate if bytes are a readable PDF and return type and page count."""
    try:
        pdf_doc = fitz.open(stream=io.BytesIO(document_bytes), filetype="pdf")
        page_count = len(pdf_doc)
        
        # Explicitly try to load the first page to ensure the file structure is valid
        # This catches malformed files that fitz.open() accepts but are actually broken
        if page_count > 0:
            try:
                pdf_doc.load_page(0) 
            except Exception as e:
                raise UnreadableFile(f"PDF is corrupted or has unreadable pages: {e}")
        else:
             raise UnreadableFile("PDF document has no pages.")
             
        pdf_doc.close()
        return "pdf", page_count
    except Exception as e:
        error_msg = str(e).lower()
        if "encrypted" in error_msg or "password" in error_msg:
            raise UnreadableFile(f"PDF is encrypted or password protected: {e}")
        # If we manually raised UnreadableFile above, re-raise it
        if isinstance(e, UnreadableFile):
            raise
        raise UnsupportedFormat("Not a valid PDF file.")


def _validate_image(document_bytes: bytes) -> Tuple[str, int]:
    """Validate if bytes are a readable image and return type and page count."""
    try:
        img = Image.open(io.BytesIO(document_bytes))
        img.verify()  # Verifies integrity, can raise exceptions.

        # Re-open after verify as verify can invalidate the stream
        img = Image.open(io.BytesIO(document_bytes))
        img_format = img.format.lower() if img.format else ""
        img.close()

        if img_format in ["jpeg", "jpg"]:
            return "jpeg", 1
        elif img_format == "png":
            return "png", 1
        else:
            # Pillow might read other formats; we only support these.
            raise UnsupportedFormat(
                f"Image format '{img_format}' is not supported. Must be JPEG or PNG."
            )
    except Exception as e:
        raise UnsupportedFormat(f"Not a valid or supported image file: {e}")


def validate_document(document_base64: str) -> Tuple[bytes, str, int]:
    """
    Validate document format and return document bytes, file type, and page count.

    Supported formats: pdf, jpeg, png

    Args:
        document_base64: Base64 encoded document string

    Returns:
        Tuple[bytes, str, int]: (document_bytes, file_type, page_count).

    Raises:
        UnsupportedFormat: If document is not pdf, jpeg, or png
        UnreadableFile: If document is corrupted or encrypted
    """
    try:
        # Decode base64
        document_bytes = base64.b64decode(document_base64)

        if len(document_bytes) == 0:
            raise UnreadableFile("Document is empty")

        try:
            # Try validating as PDF first
            return document_bytes, *_validate_pdf(document_bytes)
        except UnsupportedFormat:
            # Not a PDF, try other formats
            try:
                # Try validating as an image
                return document_bytes, *_validate_image(document_bytes)
            except UnsupportedFormat:
                # If all checks fail, the format is not supported
                raise UnsupportedFormat(
                    "Document format not supported. Must be PDF, JPEG, PNG, or TXT."
                )

    except UnsupportedFormat:
        raise
    except UnreadableFile:
        raise
    except Exception as e:
        # Catches base64 decoding errors or other unexpected issues
        raise UnreadableFile(f"Document is unreadable or corrupted: {e}")
