# =============================================================================
# APPLICATION LAYER IMPORTS
# =============================================================================
from app.application.schemas.schema import *
from app.application.swagger.swagger_config import SWAGGER_SECURITY_CONFIG


def setup_swagger_schemas(app, swagger):
    components = {
        "schemas": {
            "QueryPageResult": QueryPageResult.model_json_schema(ref_template="#/components/schemas/{model}"),
            "QueryResult": QueryResult.model_json_schema(ref_template="#/components/schemas/{model}"),
            "QueriesAggregatedResults": QueriesAggregatedResults.model_json_schema(ref_template="#/components/schemas/{model}"),
            "PollThresholdCheckResultRequest": PollThresholdCheckResultRequest.model_json_schema(ref_template="#/components/schemas/{model}"),
            "PollThresholdCheckResultResponse": PollThresholdCheckResultResponse.model_json_schema(ref_template="#/components/schemas/{model}")
        },
        "securitySchemes": SWAGGER_SECURITY_CONFIG
    }

    # Optional cleanup (harmless if nothing to delete)
    for _, schema in components["schemas"].items():
        if "$defs" in schema:
            del schema["$defs"]

    app.config.setdefault("SWAGGER", {}).update({"components": components})
    if hasattr(swagger, "config"):
        swagger.config["components"] = components

