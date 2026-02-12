# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import traceback
import os
# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
from flask import jsonify
from flasgger import Swagger
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.swagger.swagger_config import SWAGGER_CONFIG

# ---------------------- RATE LIMITER ------------------------
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
rate_limit_value = os.getenv('API_RATE_LIMIT')


# ---------------------- CORS ------------------------
def add_cors(app, allowed_origins=None):
    """
    Add CORS (Cross-Origin Resource Sharing) support to the Flask app.
    
    Args:
        app: The Flask application instance
        allowed_origins: List of allowed origins, defaults to ["*"] if None
    """
    if allowed_origins is None:
        allowed_origins = ["*"]
    CORS(app, origins=allowed_origins, supports_credentials=True)


# ---------------------- EXCEPTION HANDLER ------------------------
def unhandled_exception_handler(e):
    """
    Handle unhandled exceptions with detailed error logging.
    
    Args:
        e: The exception that was raised
        
    Returns:
        tuple: JSON error response and status code 500
    """
    error_trace = traceback.format_exc()
    print("🔥 Unhandled exception:\n" + error_trace)
    return jsonify({
        "detail": "Internal Server Error",
        "trace": error_trace
    }), 500


def init_app(app):
    """
    Initialize Flask application with extensions and configurations.
    
    Args:
        app: The Flask application instance
        
    Returns:
        Swagger: The configured Swagger instance
    """
    app.config["RATELIMIT_HEADERS_ENABLED"] = True
    app.config['SWAGGER'] = SWAGGER_CONFIG
    swagger = Swagger(app)
    # limiter.init_app(app)  # Disabled for Cloud Functions
    add_cors(app)
    return swagger
