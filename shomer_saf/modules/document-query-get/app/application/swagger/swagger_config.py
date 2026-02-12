SWAGGER_SECURITY_CONFIG = {
    "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
}

SWAGGER_CONFIG = {
    "title": "Document Query Get API",
    "uiversion": 3,
    "openapi": "3.0.3",
    "specs_route": "/apidocs/",
    "headers": [
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "GET, POST"),
    ],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "info": {
        "title": "Document Query Get API",
        "description": "API for polling threshold check results and retrieving query responses",
        "version": "1.0.0",
        "contact": {"name": "API Support", "url": "http://your-support-site.com"},
    },
}

EXAMPLE_RESULT = {
    "RequestErrorCode": 200,
    "RequestErrorMessage": "OK",
    "QueriesPageResults": [
        {
            "queryID": "1",
            "page": "1",
            "response": "model response",
            "compliance": "True",
            "confidence": "0.9",
        }
    ],
    "QueriesResults": [{"queryID": "1", "compliance": "True"}],
    "QueriesAggregatedResults": {
        "total_queries": 5,
        "true_queries": 2,
        "false_queries": 3,
    },
}
