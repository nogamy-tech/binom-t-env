# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
from flask import jsonify, request
from pydantic import ValidationError as PydanticValidationError


class APIError(Exception):
    """
    Base exception class for API-related errors.
    
    This class provides a standardized way to handle API errors with
    consistent error formatting and status codes.
    """

    def __init__(self, message, status_code=400, error_code=None, details=None):
        """
        Initialize API error with message and status information.
        
        Args:
            message: Error message
            status_code: HTTP status code (default: 400)
            error_code: Custom error code (default: HTTP_{status_code})
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or f"HTTP_{status_code}"
        self.details = details

    def to_dict(self):
        """
        Convert error to dictionary format for JSON response.
        
        Returns:
            dict: Error information in dictionary format
        """
        return {
            'error': {
                'status_code': self.status_code,
                'code': self.error_code,
                'message': self.message,
                'details': self.details,
                'endpoint': request.path,
            }
        }


# Predefined error types (add more as needed)
class BusinessRuleError(APIError):
    """
    Exception raised when business rules fail.
    
    This error is triggered when invalid user input or business logic
    validation fails.
    """
    def __init__(self, message, details=None):
        """
        Initialize business rule error.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, 400, "BUSINESS_ERROR", details)


class UnauthorizedError(APIError):
    """
    Exception raised when authentication fails.
    """
    def __init__(self, message="Unauthorized", details=None):
        super().__init__(message, 401, "UNAUTHORIZED", details)


class ValidationError(APIError):
    """
    Exception raised when validation fails.
    """
    def __init__(self, message="Validation Error", details=None):
        super().__init__(message, 422, "VALIDATION_ERROR", details)


class InternalServerError(APIError):
    """
    Exception raised for internal server errors.
    """
    def __init__(self, message="Internal Server Error", details=None):
        super().__init__(message, 500, "INTERNAL_SERVER_ERROR", details)


# DocumentPageProcessing specific errors
class GCPBucketError(APIError):
    """461 - Bucket Error - GCS bucket does not exist"""
    def __init__(self, message="Bucket Error", details=None):
        super().__init__(message, 461, "BUCKET_NOT_EXISTS", details)


class GCPBucketTimeoutError(APIError):
    """462 - Bucket Timeout - Upload timeout to GCS"""
    def __init__(self, message="Bucket Timeout", details=None):
        super().__init__(message, 462, "BUCKET_TIMEOUT", details)


class GCPFileExistsError(APIError):
    """463 - File Exists - File already exists in GCS bucket"""
    def __init__(self, message="No Document In Bucket", details=None):
        super().__init__(message, 463, "NO_DOCUMENT_IN_BUCKET", details)


class DocumentAIError(APIError):
    """464 - Document AI processing failure"""
    def __init__(self, message="Document AI Error", details=None):
        super().__init__(message, 464, "DOCUMENT_AI_FAILURE", details)


class DocumentAITimeoutError(APIError):
    """465 - Document AI did not respond in time"""
    def __init__(self, message="Document AI Timeout", details=None):
        super().__init__(message, 465, "DOCUMENT_AI_TIMEOUT", details)


class UnsupportedFormatError(APIError):
    """466 - Image quality invalid"""
    def __init__(self, message="Image Quality Invalid", details=None):
        super().__init__(message, 466, "IMG_QUALITY_INVALID", details)


# Register handlers with Flask
def register_error_handlers(app):
    """
    Register error handlers with Flask application.
    
    Args:
        app: The Flask application instance
    """
    # Handle Pydantic validation errors (422) - Matches your format
    @app.errorhandler(PydanticValidationError)
    def handle_pydantic_error(err):
        return jsonify({
            'error': {
                'status_code': 422,
                'code': 'SCHEMA_ERROR',
                'message': 'Unprocessable Entity',
                'details': err.errors(),
                'endpoint': request.path
            }
        }), 422

    # Handle standard HTTP errors (400, 401, 404, 500, etc.)
    @app.errorhandler(400)
    def handle_400(err):
        return jsonify({
            'error': {
                'status_code': 400,
                'code': 'BAD_REQUEST',
                'message': 'Bad request',
                'details': str(err.description) if err.description else None,
                'endpoint': request.path
            }
        }), 400

    @app.errorhandler(401)
    def handle_401(err):
        return jsonify({
            'error': {
                'status_code': 401,
                'code': 'UNAUTHORIZED',
                'message': 'Unauthorized',
                'details': str(err.description) if err.description else None,
                'endpoint': request.path
            }
        }), 401

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({
            'error': {
                'status_code': 404,
                'code': 'NOT_FOUND',
                'message': 'Resource not found',
                'details': str(err.description) if err.description else None,
                'endpoint': request.path
            }
        }), 404

    @app.errorhandler(500)
    def handle_500(err):
        return jsonify({
            'error': {
                'status_code': 500,
                'code': 'SERVER_ERROR',
                'message': 'Internal server error',
                'details': str(err.description) if err.description else None,
                'endpoint': request.path
            }
        }), 500

    # Handle APIErrors (your custom errors) - Already matches your format
    @app.errorhandler(APIError)
    def handle_api_error(err):
        return jsonify(err.to_dict()), err.status_code

    # Catch-all for unexpected errors
    @app.errorhandler(Exception)
    def handle_unexpected_error(err):
        return jsonify({
            'error': {
                'status_code': 500,
                'code': 'UNEXPECTED_ERROR',
                'message': 'An unexpected error occurred',
                'details': str(err),
                'endpoint': request.path
            }
        }), 500