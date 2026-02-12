# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================

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
from app.application.schemas.schema import (
    QueueThresholdCheckRequest,
    QueueThresholdCheckResponse,
)
from app.application.swagger.swagger_docs import (
    queue_threshold_check_docs,
    health_check_docs,
)
from app.application.errors.errors_class import APIError
from app.application.errors.errors_mapping import ERROR_MAP, get_error_class_for_message
# =============================================================================
# LOGIC LAYER IMPORTS
# =============================================================================


# Define a blueprint
document_start_job_bp = Blueprint("document_start_job", __name__)


@document_start_job_bp.route("/health-check", methods=["GET"])
@swag_from(health_check_docs)
def health_check():
    return make_response(jsonify({"status": "success"}), 200)


@document_start_job_bp.route("/queue-threshold-checks", methods=["POST"])
@limiter.limit(rate_limit_value)
@swag_from(queue_threshold_check_docs)
def queue_threshold_check():
    try:
        # Get headers
        x_client_id = request.headers.get("x-client-id")
        x_client_secret = request.headers.get("x-client-secret")
        x_scope = request.headers.get("x-scope")

        # Validate required headers
        if not x_client_id:
            raise APIError("x-client-id header is required", 400, "MISSING_HEADER")
        if not x_scope:
            raise APIError("x-scope header is required", 400, "MISSING_HEADER")

        payload = request.get_json(silent=True)
        request_message = QueueThresholdCheckRequest.model_validate(payload)

        request_message_dict = request_message.model_dump()

        # Add headers to the request message dict
        request_message_dict["x_client_id"] = x_client_id
        request_message_dict["x_client_secret"] = x_client_secret
        request_message_dict["x_scope"] = x_scope

        # ---- call service ----
        logic = current_app.config["DOC_START_JOB_LOGIC"]
        code, message = logic.run_process(request_message_dict)

        # ---- errors (raise class HERE based on code) ----
        if code != 200:
            ErrCls = get_error_class_for_message(code, message)
            if ErrCls:
                raise ErrCls(message)  # message/status/details live inside your class
            abort(code)

        # success
        response_body = QueueThresholdCheckResponse(
            RequestErrorCode=code, RequestErrorMessage=message
        ).model_dump()

        return make_response(jsonify(response_body), 200)

    except PydanticValidationError:
        raise  # let your 422 handler format it
    except APIError:
        raise
    except Exception:
        abort(500)
