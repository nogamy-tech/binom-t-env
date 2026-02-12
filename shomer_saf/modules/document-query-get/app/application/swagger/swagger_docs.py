# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_helpers import generate_error_responses
from app.application.swagger.swagger_config import EXAMPLE_RESULT


poll_threshold_check_result_docs = {
    "tags": ["Document Query Get"],
    "x-tags": {
        "officeName": "Authority for Computerization",
        "databseName": "Document Processing",
        "subject": "Document Processing Service",
        "serviceType": "Processing",
        "version": "v1",
        "publisherType": "Government"
    },
    "summary": "Poll threshold check results",
    "description": "Retrieves query results for a document processing job by ClientRequestId.",
    "operationId": "pollThresholdCheckResult",
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
                "schema": {
                    "$ref": "#/components/schemas/PollThresholdCheckResultRequest"
                }
            }
        },
    },
    "responses": {
        "200": {
            "description": "Query results retrieved successfully",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/PollThresholdCheckResultResponse"
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
    "tags": ["Document Query Get"],
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
