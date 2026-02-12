# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_helpers import generate_error_responses

document_validation_docs = {
    "tags": ["Document Process Query"],
    "summary": "Process document query",
    "description": "Process a user query against a specific document page using AI models",
    "operationId": "documentProcessQuery",

    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/DocumentProcessRequest"}
            }
        }
    },
    "responses": {
        "200": {
            "description": "Query processed successfully",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/DocumentProcessResponse"}
                }
            }
        },
        **generate_error_responses()
    },
    "security": [{"bearerAuth": []}]
}