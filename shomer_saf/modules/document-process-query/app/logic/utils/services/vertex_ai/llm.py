# libraries
import google.api_core.exceptions
import requests
import socket
from google.genai import types
from pathlib import Path
from typing import Optional, Union
import imghdr

# modules
from .utils import LLMResponse, render_prompt, parse_as_json
from .custom_errors import VisionModelTimeOut, TextModelTimeOut, ModelFailure
from ..gcp_client import GCPServiceFactory


class LLM:
    """
    A unified class to interact with Google's Gemini models for both text and image queries.
    """

    def __init__(
        self,
        gcp_factory: GCPServiceFactory,
        prompt_path: Union[str, Path],
        text_model_name: str,
        image_model_name: str,
    ):
        """
        Initializes the LLM client.

        Args:
            gcp_factory (GCPServiceFactory): An instance of the GCP client factory.
            prompt_path (Union[str, Path]): The path to the base prompt template.
            text_model_name (str): The name of the text model to use.
            image_model_name (str): The name of the image model to use.
        """
        self.client = gcp_factory.get_gcp_client("gemini")
        self.prompt_path = prompt_path
        self.text_model_name = text_model_name
        self.image_model_name = image_model_name

    def query(self, user_query: str, context: Union[str, bytes], few_shots: Optional[str] = "") -> LLMResponse:
        """
        Queries a Gemini model with the given context (text or image).

        Args:
            user_query (str): The main user query or instruction.
            context (Union[str, bytes]): The context for the query, either a string (text) or bytes (image).
            few_shots (Optional[str], optional): Few-shot examples. Defaults to an empty string.

        Returns:
            LLMResponse: A structured response object.

        Raises:
            ValueError: If the context type is not supported.
            VisionModelTimeOut: If an image query times out.
            TextModelTimeOut: If a text query times out.
            ModelFailure: For other model-related errors.
        """
        base_prompt_path = self.prompt_path

        # * Text
        if isinstance(context, str):
            # Handle Text Query
            model_name = self.text_model_name
            full_prompt = render_prompt(base_prompt_path, context, user_query, few_shots)

            try:
                response = self.client.models.generate_content(model=model_name, contents=full_prompt)
            except (requests.exceptions.Timeout, socket.timeout) as e:
                raise TextModelTimeOut(f"Gemini model request timed out: {e}")
            except google.api_core.exceptions.DeadlineExceeded as e:
                raise TextModelTimeOut(f"Gemini model request deadline exceeded: {e}")
            except Exception as e:
                raise ModelFailure(f"Error querying Gemini text model: {e}")

        # * Image
        elif isinstance(context, bytes):
            # Handle Image Query
            model_name = self.image_model_name

            image_type = imghdr.what(None, h=context)
            if image_type not in ("png", "jpeg", "jpg", "tiff"):
                raise ValueError("Unsupported image type. Only PNG, TIFF, and JPEG are supported.")

            mime_type = f"image/{'jpeg' if image_type == 'jpg' else image_type}"
            image_part = types.Part.from_bytes(data=context, mime_type=mime_type)

            full_prompt = render_prompt(template_path=base_prompt_path, context="[Image context provided]", query=user_query, few_shots=few_shots)

            try:
                response = self.client.models.generate_content(model=model_name, contents=[image_part, full_prompt])
            except (requests.exceptions.Timeout, socket.timeout) as e:
                raise VisionModelTimeOut(f"Gemini model request timed out: {e}")
            except google.api_core.exceptions.DeadlineExceeded as e:
                raise VisionModelTimeOut(f"Gemini model request deadline exceeded: {e}")
            except Exception as e:
                raise ModelFailure(f"Error querying Gemini image model: {e}")

        else:
            raise ValueError(f"Unsupported context type: {type(context)}")

        return parse_as_json(response.text)
