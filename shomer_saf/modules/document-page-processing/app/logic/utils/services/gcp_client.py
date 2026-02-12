import google.auth
import importlib
import inspect


class GCPServiceFactory:
    """
    A factory class to create and manage Google Cloud Platform (GCP) service clients.

    This class centralizes the logic for initializing various GCP clients,
    handling authentication, and applying service-specific configurations.
    """

    SERVICE_CLIENTS = {
        # Vertex AI
        "vertex_ai_prediction": (
            "google.cloud.aiplatform.gapic",
            "PredictionServiceClient",
        ),
        # Document AI (v1)
        "document_ai": ("google.cloud.documentai_v1", "DocumentProcessorServiceClient"),
        # Storage (Buckets)
        "storage": ("google.cloud", "storage.Client"),
        # Secret Manager
        "secret_manager": ("google.cloud.secretmanager", "SecretManagerServiceClient"),
        # Workflows
        "workflows": ("google.cloud.workflows", "WorkflowsClient"),
        "workflow_executions": (
            "google.cloud.workflows.executions_v1",
            "ExecutionsClient",
        ),
        # BigQuery
        "bigquery": ("google.cloud", "bigquery.Client"),
        # Logging
        "logging": ("google.cloud.logging_v2", "LoggingServiceV2Client"),
        # Firestore / Datastore
        "firestore": ("google.cloud.firestore", "Client"),
        "datastore": ("google.cloud.datastore", "Client"),
        # Gemini / Google Gen AI
        "gemini": ("google.genai", "Client"),
    }

    def __init__(self):
        """
        Initializes the GCPServiceFactory by authenticating with GCP
        and retrieving the default project ID.
        """
        self.credentials, self.project_id = google.auth.default()

    def get_gcp_client(self, service: str, **kwargs):
        """
        Return a GCP client for a given service.

        Args:
            service (str): The name of the GCP service for which to get a client.
            **kwargs: Additional keyword arguments for service-specific configurations.

        Special cases:
            - Firestore: pass 'database' to specify Firestore database (default is '(default)')
            - Gemini: Always uses Vertex AI (ADC), project auto-detected,
                      location forced to 'europe-west1'

        Returns:
            An initialized GCP service client.

        Raises:
            ValueError: If the requested service is not supported.
        """
        if service not in self.SERVICE_CLIENTS:
            raise ValueError(
                f"Unsupported service '{service}'. Supported: {list(self.SERVICE_CLIENTS)}"
            )

        module_path, class_path = self.SERVICE_CLIENTS[service]

        # Handle dotted class paths
        if "." in class_path:
            mod_name, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(f"{module_path}.{mod_name}")
        else:
            module = importlib.import_module(module_path)
            class_name = class_path

        client_cls = getattr(module, class_name)

        sig = inspect.signature(client_cls.__init__)
        params = sig.parameters

        args = {"credentials": self.credentials}
        if "project" in params:
            args["project"] = self.project_id

        # === Firestore special handling for database parameter ===
        if service == "firestore":
            database = kwargs.pop("database", "(default)")
            # Initialize Firestore client
            client = client_cls(**args)
            # Add custom database path attribute
            client._database_string_internal = (
                f"projects/{self.project_id}/databases/{database}"
            )
            return client

        # Document AI: custom endpoint per region
        if service == "document_ai":
            region = kwargs.pop("region", "us")  # default to 'us'
            client_options = {"api_endpoint": f"{region}-documentai.googleapis.com"}
            args["client_options"] = client_options

        # Gemini special handling
        if service == "gemini":
            location = kwargs.pop("location", "us-central1")
            return client_cls(vertexai=True, project=self.project_id, location=location)

        return client_cls(**args)

    def get_projectid(self):
        """
        Returns the default GCP project ID.

        Returns:
            str: The GCP project ID.
        """
        return self.project_id
