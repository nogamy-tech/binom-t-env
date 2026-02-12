# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_class import APIError


# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_class import APIError


def generate_error_responses():
    """
    Generate error response schemas for Swagger documentation.
    
    Returns:
        dict: Dictionary containing error response schemas for different HTTP status codes
    """

    error_codes = [
        400, 401, 422, 461, 462, 463, 464, 465, 466, 500
    ]

    responses = {}

    for code in error_codes:
        try:
            # Find the class for this code
            error_class = next(
                cls for cls in APIError.__subclasses__()
                if cls(None, code).status_code == code
            )
            example = error_class().to_dict()
        except:
            example = {
                'error': {
                    'code': f"HTTP_{code}",
                    'message': "Error occurred",
                    'details': None,
                    'endpoint': "/example"
                }
            }

        responses[str(code)] = {
            "description": f"Error {code}",
            "content": {
                "application/json": {"example": example}
            }
        }

    return responses