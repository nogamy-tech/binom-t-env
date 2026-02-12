# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from datetime import datetime, timezone

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
from flask import Blueprint, request, jsonify, abort, make_response, current_app
from flasgger import swag_from
from pydantic import ValidationError as PydanticValidationError

# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.utils.helpers import calculate_duration
from app.application.utils.extension import limiter, rate_limit_value
from app.application.schemas.schema import DocumentProcessRequest, DocumentProcessResponse
from app.application.swagger.swagger_docs import document_validation_docs
from app.application.errors.errors_class import APIError
from app.application.errors.errors_mapping import ERROR_MAP
# =============================================================================
# LOGIC LAYER IMPORTS
# =============================================================================


# Define a blueprint
document_process_query_bp = Blueprint("document_process_query", __name__)


@document_process_query_bp.route("/Document/ProcessQuery", methods=["POST"])
@limiter.limit(rate_limit_value)
@swag_from(document_validation_docs)  # Using shared/swagger.py
def document_query():
    try:
        payload = request.get_json(silent=True)
        request_message = DocumentProcessRequest.model_validate(payload)

        request_message_dict = request_message.model_dump()

        # ---- call service ----
        
        logic = current_app.config["DOC_PROCESSQUERY_LOGIC"]
        code, message,llm_response = logic.run_process(request_message_dict)

        # Calculate duration
        duration = calculate_duration(request_message.Timestamp)

        # ---- errors (raise class HERE based on code) ----
        if code != 200:
            ErrCls = ERROR_MAP.get(code)
            if ErrCls:
                raise ErrCls()  # message/status/details live inside your class
            abort(code)

        # success
        response_body = DocumentProcessResponse(
            RequestErrorCode=code,
            RequestErrorMessage=message,
            LLMResponse=llm_response
        ).model_dump()

        return make_response(jsonify(response_body), 200)

    except PydanticValidationError:
        raise  # let your 422 handler format it
    except APIError:
        raise
    except Exception:
        abort(500)