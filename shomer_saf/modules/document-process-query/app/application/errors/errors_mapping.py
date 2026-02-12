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
    463: DataMissingError,  # DATA_MISSING
    467: TextModelTimeoutError,  # TEXT_MODEL_TIMEOUT
    468: VisionModelTimeoutError,  # VISION_MODEL_TIMEOUT
    469: ModelFailureError,  # MODEL_FAILURE
    470: DBTimeoutError,  # DB_TIMEOUT
    500: InternalServerError,
}
