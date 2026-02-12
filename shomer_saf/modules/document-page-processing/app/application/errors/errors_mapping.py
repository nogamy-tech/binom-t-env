# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_class import *

ERROR_MAP = {
    400: BusinessRuleError,
    401: UnauthorizedError,
    422: ValidationError,
    461: GCPBucketError,  # BUCKET_NOT_EXISTS
    462: GCPBucketTimeoutError,  # BUCKET_TIMEOUT
    463: GCPFileExistsError,  # NO_DOCUMENT_IN_BUCKET
    464: DocumentAIError,  # DOCUMENT_AI_FAILURE
    465: DocumentAITimeoutError,  # DOCUMENT_AI_TIMEOUT
    466: UnsupportedFormatError,  # IMG_QUALITY_INVALID
    500: InternalServerError,
}
