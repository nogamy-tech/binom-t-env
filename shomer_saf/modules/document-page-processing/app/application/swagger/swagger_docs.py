# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_helpers import generate_error_responses

document_validation_docs = {
        "tags": ["Document Page Processing"],
        "summary": "Process document page",
        "description": "Process a specific page of a document for text or image extraction",
        "operationId": "documentPageProcessing",
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/PageProcessingRequest"}
                }
            }
        },
        "responses": {
            "202": {
                "description": "Job started successfully",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/PageProcessingResponse"}
                    }
                }
            },
            **generate_error_responses()
        },
        "security": [{"bearerAuth": []}]
    }