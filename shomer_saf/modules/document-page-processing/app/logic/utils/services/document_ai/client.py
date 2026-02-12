import base64
from google.cloud import documentai_v1 as documentai
from app.logic.utils.services.gcp_client import GCPServiceFactory

class DocumentAIClient:
    """
    A client for interacting with Google Cloud Document AI.
    """

    def __init__(self, location: str, processor_id: str, gcp_factory: GCPServiceFactory):
        """
        Initializes the Document AI client.

        Args:
            location (str): Region where the Document AI processor is hosted (e.g., "us", "eu").
            processor_id (str): The processor's unique ID.
            gcp_factory (GCPServiceFactory): An instance of the GCPServiceFactory.
        """
        self.project_id = gcp_factory.get_projectid()
        self.location = location
        self.processor_id = processor_id.split("/")[-1]
        self.gcp_factory = gcp_factory
        self.client = self._create_documentai_client()
        self.resource_name = self._get_resource_name()

    def _create_documentai_client(self) -> documentai.DocumentProcessorServiceClient:
        """Creates a Document AI client."""
        return self.gcp_factory.get_gcp_client("document_ai", region=self.location)

    def _get_resource_name(self) -> str:
        """
        Constructs the full resource name for a Document AI processor.
        """
        return self.client.processor_path(self.project_id, self.location, self.processor_id)

    def process_file(self, file_base64: str, mime_type: str) -> str:
        """
        Sends a document to Document AI for text extraction.

        Args:
            file_base64 (str): Base64-encoded content of the document.
            mime_type (str): MIME type of the file.

        Returns:
            str: The extracted text from the document.
        """
        content = base64.b64decode(file_base64)

        raw_document = documentai.RawDocument(content=content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=self.resource_name, raw_document=raw_document)
        result = self.client.process_document(request=request, timeout=600)
        return result.document.text
