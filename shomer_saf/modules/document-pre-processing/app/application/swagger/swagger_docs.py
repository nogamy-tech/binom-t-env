# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_helpers import generate_error_responses
from app.application.swagger.swagger_config import EXAMPLE_RESULT


document_preprocessing_docs = {
    "tags": ["Document PreProcessing"],
    "summary": "Process documents for preprocessing",
    "description": "Process documents for preprocessing with specified bucket paths and transaction ID.",
    "operationId": "documentPreProcessing",

    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/DocumentPreProcessingRequest"}
            }
        }
    },
    "responses": {
        "200": {
            "description": "Document preprocessing completed successfully",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/DocumentPreProcessingResponse"},
                    "example": EXAMPLE_RESULT
                }
            }
        },
        **generate_error_responses()
    },
    "security": []
}