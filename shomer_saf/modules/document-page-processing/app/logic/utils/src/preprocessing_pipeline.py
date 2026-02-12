import base64
from google.api_core.exceptions import DeadlineExceeded, GoogleAPICallError, ServiceUnavailable, InvalidArgument
from app.logic.utils.services.document_ai import DocumentAIClient,custom_errors as ce


def preprocess_text(docai_client: DocumentAIClient, file_base64: str, mime_type: str) -> str:
    try:
        text = docai_client.process_file(file_base64=file_base64, mime_type=mime_type)

        base64_text = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        return base64_text

    except DeadlineExceeded:
        raise ce.DocumentAITimeout(" Document AI request timed out.")
    except InvalidArgument as e:
        raise ce.DocumentAIFailure(f" Invalid input to Document AI: {e}")
    except ServiceUnavailable:
        raise ce.DocumentAIFailure(" Document AI service is currently unavailable.")
    except GoogleAPICallError as e:
        raise ce.DocumentAIFailure(f" Document AI API call failed: {e}")
    except Exception as e:
        raise ce.DocumentAIFailure(f" Unexpected error in Document AI pipeline: {e}")


# TODO : implement logic for preprocessing images
def preprocess_image(docai_client: DocumentAIClient, file_base64: str, mime_type: str) -> str:
    """PLACEHOLDER"""
    try:
        return file_base64
    except Exception as e:
        raise ce.ImgQualityInvalid(f"Invalid image quality. {e}")
