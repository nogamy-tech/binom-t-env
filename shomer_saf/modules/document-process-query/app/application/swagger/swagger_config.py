SWAGGER_SECURITY_CONFIG = {
    "bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}

SWAGGER_CONFIG = {
                    'title': 'Document Process Query API',
                    'uiversion': 3,
                    'openapi': '3.0.3',
                    'specs_route': '/apidocs/',
                    'headers': [('Access-Control-Allow-Origin', '*'),
                                ('Access-Control-Allow-Methods', "GET, POST")],
                    'specs': [
                        {'endpoint': 'apispec',
                         'route': '/apispec.json',
                         'rule_filter': lambda rule: True,
                         'model_filter': lambda tag: True}],
                    'info': {
                        'title': "Document Process Query API",
                        'description': "API for processing user queries against document pages using AI models",
                        'version': "1.0.0",
                        'contact': {'name': "API Support",
                                    'url': "http://your-support-site.com"}
                    }
                }

