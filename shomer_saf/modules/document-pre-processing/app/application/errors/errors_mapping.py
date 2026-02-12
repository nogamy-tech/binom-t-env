# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.errors.errors_class import *

ERROR_MAP = {
    400: BusinessRuleError,
    461: DocumentsBucketFolderNotExistsError,  # DocumentsBucketFolder doesn't exist (also used for PagesBucketFolder)
    462: DocumentsBucketFolderTimeoutError,    # DocumentsBucketFolder timeout
    463: DocumentExistsError,                  # Document exists or multiple documents
}
