# libraries
from typing import List
import base64
import io
from PIL import Image

# from pdf2image import convert_from_bytes
import pypdfium2

# modules
from .convertion_funcs import convert_docx_bytes_to_pdf_bytes, process_pdf_bytes, process_image_bytes


def split_file_to_pages(file_bytes: bytes, file_type: str) -> List[str]:
    """
    Splits a document or image file into individual pages.

    Supports DOCX, PDF, JPEG/JPG, PNG, and TXT formats. DOCX files are first
    converted to PDF before processing. Each returned page is represented
    as a base64-encoded string.

    Args:
        file_bytes: Raw file content as bytes .
        file_type: File type or extension (e.g., '.pdf', '.docx', 'jpeg', '.txt').

    Returns:
        List[str]: A list of page contents in base64 format, one per page.
    """
    ext = file_type.lower()

    if "docx" in ext:
        # Convert docx -> pdf -> process
        pdf_bytes = convert_docx_bytes_to_pdf_bytes(docx_bytes=file_bytes)
        pages = process_pdf_bytes(pdf_bytes=pdf_bytes)

    elif "pdf" in ext:
        pages = process_pdf_bytes(pdf_bytes=file_bytes)

    elif "jpeg" in ext or "jpg" in ext:
        pages = process_image_bytes(image_bytes=file_bytes, conversion_format="jpeg")

    elif "png" in ext:
        pages = process_image_bytes(image_bytes=file_bytes, conversion_format="png")

    # --- ADDED TXT COMPATIBILITY HERE ---
    elif "txt" in ext or "text" in ext:
        # For a TXT file, treat the entire content as a single "page"
        # and encode the raw bytes to base64.
        base64_content = base64.b64encode(file_bytes).decode("utf-8")
        pages = [base64_content]

    return pages


def convert_to_tiff(base64_str: str) -> bytes:
    """
    Converts a base64-encoded single-page file (image or PDF) to TIFF format in bytes.

    Args:
        base64_str (str): Base64-encoded single-page file (image or one-page PDF).

    Returns:
        bytes: TIFF file in bytes.
    """
    # Decode base64 string to raw bytes
    file_bytes = base64.b64decode(base64_str)
    file_io = io.BytesIO(file_bytes)

    try:
        # Try to open directly as an image
        with Image.open(file_io) as img:
            img_rgb = img.convert("RGB")
            tiff_io = io.BytesIO()
            img_rgb.save(tiff_io, format="TIFF")
            return tiff_io.getvalue()

    except Exception:
        # If it's not an image, assume it's a one-page PDF
        pdf = pypdfium2.PdfDocument(io.BytesIO(file_bytes))
        page = pdf[0]
        # Render the first page to a PIL image
        pil_image = page.render(scale=2).to_pil()  # scale=2 for better resolution

        tiff_io = io.BytesIO()
        pil_image.convert("RGB").save(tiff_io, format="TIFF")
        return tiff_io.getvalue()
