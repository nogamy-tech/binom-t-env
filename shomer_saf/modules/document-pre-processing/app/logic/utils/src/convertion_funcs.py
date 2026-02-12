# libraries
from typing import List
import base64
import fitz
import io
from PIL import Image
from docx2pdf import convert
import tempfile
import os


def process_pdf_bytes(pdf_bytes: bytes) -> List[str]:
    """
    Splits a PDF (provided as raw bytes) into single-page PDFs,
    and returns each page as a base64-encoded string.

    Args:
        pdf_bytes (bytes): Raw bytes of the PDF file.

    Returns:
        list[str]: List of base64-encoded strings, each representing a single page PDF.
    """
    # Open the PDF from bytes
    doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")

    pages = []
    for page_num in range(len(doc)):
        # Create a new empty PDF for a single page
        single_page_pdf = fitz.open()
        single_page_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)

        # Get bytes of this single-page PDF
        single_page_bytes = single_page_pdf.tobytes()

        # Encode it as base64
        b64_page = base64.b64encode(single_page_bytes).decode("utf-8")
        pages.append(b64_page)

    return pages


def process_image_bytes(image_bytes: bytes, conversion_format: str) -> List[str]:
    """
    Processes an image (or multi-frame image) provided as raw bytes, converts each frame
    to the specified format, and returns a list of base64-encoded strings for each frame.

    Args:
        image_bytes (bytes): Raw bytes of the image file.
        conversion_format (str): Format to convert each frame/page (e.g., "PNG", "JPEG").

    Returns:
        list[str]: List of base64-encoded strings, one per frame/page of the image.
    """
    image = Image.open(io.BytesIO(image_bytes))

    pages = []
    try:
        i = 0
        while True:
            image.seek(i)
            with io.BytesIO() as output:
                image.save(output, format=conversion_format)
                img_bytes = output.getvalue()
                b64_page = base64.b64encode(img_bytes).decode("utf-8")
                pages.append(b64_page)
            i += 1
    except EOFError:
        # No more frames
        pass

    return pages


def convert_docx_bytes_to_pdf_bytes(docx_bytes: bytes) -> bytes:
    """
    Converts a DOCX file (provided as raw bytes) to PDF bytes.

    Args:
        docx_bytes (bytes): Raw bytes of the DOCX file.

    Returns:
        bytes: PDF file content as bytes.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        docx_path = os.path.join(tmpdir, "input.docx")
        pdf_path = os.path.join(tmpdir, "output.pdf")

        # Save DOCX bytes to temporary file
        with open(docx_path, "wb") as f:
            f.write(docx_bytes)

        # Convert DOCX to PDF
        convert(docx_path, pdf_path)

        # Read PDF back as bytes
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

    return pdf_bytes
