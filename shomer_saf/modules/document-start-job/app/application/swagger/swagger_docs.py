# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_helpers import generate_error_responses
from app.application.swagger.swagger_config import EXAMPLE_RESULT


queue_threshold_check_docs = {
    "tags": ["Document Start Job"],
    "x-tags": {
        "officeName": "Authority for Computerization",
        "databseName": "Document Processing",
        "subject": "Document Processing Service",
        "serviceType": "Processing",
        "version": "v1",
        "publisherType": "Government"
    },
    "summary": "Queue threshold check for document processing",
    "description": "Validates input, checks accounts, validates document, saves to bucket, creates DB records, and triggers workflow.",
    "operationId": "queueThresholdCheck",
    "parameters": [
        {
            "name": "x-client-id",
            "in": "header",
            "required": True,
            "schema": {"type": "string"},
            "description": "The client identifier",
        },
        {
            "name": "x-client-secret",
            "in": "header",
            "required": False,
            "schema": {"type": "string"},
            "description": "The client secret",
        },
        {
            "name": "x-scope",
            "in": "header",
            "required": True,
            "schema": {"type": "string"},
            "description": "The scope identifier",
        },
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/QueueThresholdCheckRequest"}
            }
        },
    },
    "responses": {
        "200": {
            "description": "Request accepted and processing started",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/QueueThresholdCheckResponse"
                    },
                    "example": EXAMPLE_RESULT,
                }
            },
        },
        **generate_error_responses(),
    },
    "security": [],
}


health_check_docs = {
    "tags": ["Document Start Job"],
    "summary": "Health check for document processing",
    "description": "Returns a success message if the service is running.",
    "operationId": "healthCheck",
    "responses": {
        "200": {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"}
                        },
                    }
                }
            },
        }
    },
}
