# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import os

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
import functions_framework
from flask import Flask, jsonify
 
# =============================================================================
# PROJECT CONFIGURATION IMPORTS
# =============================================================================
from app.dotenv import base_dir, data_dir

# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.swagger.swagger_setup import setup_swagger_schemas
from app.application.utils.extension import init_app, unhandled_exception_handler
from app.application.errors.errors_class import register_error_handlers, APIError
from app.application.document_pre_processing_job import document_pre_processing_bp

# =============================================================================
# LOGIC LAYER IMPORTS
# =============================================================================
from app.application.mock.mock_process import DocumentPreProcessingMockProcess
from app.logic.document_pre_processing_process import DocumentPreProcessingProcess

def create_app() -> Flask:
    """
    This function initializes the Flask app with all necessary configurations including
    Swagger documentation, error handlers, CORS, rate limiting, and blueprints.

    """

    app = Flask(__name__)

    # Blueprints (routes) - MUST be registered BEFORE Swagger
    app.register_blueprint(document_pre_processing_bp, url_prefix="/shomer-saf/PreProcessing")

    # define service to run
    # app.config["DOC_PREPROC_LOGIC"] = DocumentPreProcessingMockProcess()
    app.config["DOC_PREPROC_LOGIC"] = DocumentPreProcessingProcess()
    
    @app.route("/", methods=["GET"])
    def root():
        """
        Root endpoint that returns a simple status message.
        """
        return jsonify({"message": "Flask app is running. Go to /apidocs/ for Swagger."})

    # Swagger / Flasgger
    swagger = init_app(app)
    setup_swagger_schemas(app, swagger)

    # Errors
    register_error_handlers(app)

    # Global unhandled exception hook
    @app.errorhandler(Exception)
    def handle_exception(e):
        """
        Global exception handler for unhandled exceptions.
        """
        if isinstance(e, APIError):
            raise  # Let APIError handler deal with it
        return unhandled_exception_handler(e)

    return app


app = create_app()

@functions_framework.http
def flask_app(request):
    """
    Google Cloud Functions entry point for the Flask application.
    """
    return app(request.environ, lambda *args, **kwargs: None)



if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000)) 
    app.run(host="0.0.0.0", port=port)