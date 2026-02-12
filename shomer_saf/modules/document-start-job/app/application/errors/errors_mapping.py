# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_class import *

ERROR_MAP = {
    400: BusinessRuleError,
    422: SchemaValidationError,
    424: AccountsDBTimeoutError,  # ACCOUNTS_DB_TIMEOUT or DB_TIMEOUT
    431: UnsupportedFormatError,  # UNSUPPORTED_FORMAT
    432: UnreadableFileError,  # UNREADABLE_FILE
    460: UnknownClientError,  # UNKNOWN_CLIENT
    461: BucketNotExistsError,  # BUCKET_NOT_EXISTS
    462: BucketTimeoutError,  # BUCKET_TIMEOUT
    463: ClientRequestIdAlreadyUsedError,  # CLIENT_REQUEST_ID_ALREADY_USED
    464: WorkflowTimeoutError,  # WORKFLOW_TIMEOUT
    465: WorkflowError,  # WORKFLOW_ERROR
    500: ExternalServiceError,  # Default for 500 errors
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

