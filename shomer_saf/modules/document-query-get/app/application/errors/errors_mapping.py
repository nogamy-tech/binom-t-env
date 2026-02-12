# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_class import *

ERROR_MAP = {
    400: BusinessRuleError,
    422: SchemaValidationError,
    424: AccountsDBTimeoutError,  # ACCOUNTS_DB_TIMEOUT
    460: UnknownClientError,  # UNKNOWN_CLIENT
    424: DBTimeoutError,  # DB_TIMEOUT (Note: overlaps with AccountsDBTimeoutError, both use 424)
    500: NoContentError,  # NO_CONTENT or other 500 errors
}

def get_error_class_for_message(error_code: int, error_message: str):
    """
    Get the appropriate error class based on error code.
    
    Args:
        error_code: HTTP error code
        error_message: Error message string (not used, kept for backwards compatibility)
        
    Returns:
        Error class to raise
    """
    return ERROR_MAP.get(error_code, ExternalServiceError)

