SWAGGER_SECURITY_CONFIG = {
    "bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}

SWAGGER_CONFIG = {
                    'title': 'Document Page Processing API',
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
                        'title': "Document Page Processing API",
                        'description': "API for processing individual document pages for text or image extraction",
                        'version': "1.0.0",
                        'contact': {'name': "API Support",
                                    'url': "http://your-support-site.com"}
                    }
                }

