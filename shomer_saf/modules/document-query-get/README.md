# DocumentQueryGet

A document query get API built with Flask that handles polling threshold check results and retrieving aggregated query responses. DocumentQueryGet validates client requests, queries DocumentsQueryJobs, aggregates query results across pages, and returns comprehensive query response data.

## Description

DocumentQueryGet is designed to retrieve and aggregate query results from document processing jobs. It accepts ClientRequestId, validates client credentials, queries DocumentsQueryJobs for query responses, aggregates results across pages, and returns detailed query response information including per-page results, per-query aggregated results, and overall statistics. The service is built with a clean application layer architecture using mock processing for development and testing.

### Key Features
- **Account Validation**: Queries AccountsDB to validate client and scope
- **Query Retrieval**: Queries DocumentsQueryJobs to retrieve query responses
- **Response Aggregation**: Aggregates query responses across multiple pages
- **Result Statistics**: Provides comprehensive query result statistics
- **API Documentation**: Built-in Swagger/OpenAPI documentation
- **Error Handling**: Comprehensive error management and reporting
- **Mock Processing**: Mock implementation for development and testing

## 📁 Project Structure

```
DocumentQueryGet/
├── 📄 main.py                                  # Application entry point and Flask app configuration
├── 📄 requirements.txt                         # Python dependencies
├── 📄 main.ipynb                               # Jupyter notebook for development/testing
├── 📁 app/                                     # Main application package
│   ├── 📁 application/                         # Application layer (API, routes, schemas)
│   │   ├── 📄 document_query_get.py            # Main API endpoint and request handling
│   │   ├── 📁 errors/                          # Error handling and custom exceptions
│   │   │   ├── 📄 errors_class.py              # Custom API error classes and handlers
│   │   │   ├── 📄 errors_helpers.py            # Error response generation utilities
│   │   │   └── 📄 errors_mapping.py            # Error code to exception mapping
│   │   ├── 📁 mock/                            # Mock processing implementation
│   │   │   ├── 📄 __init__.py                  # Mock package initialization
│   │   │   └── 📄 mock_process.py              # Mock document query get logic
│   │   ├── 📁 schemas/                         # Pydantic data models and validation
│   │   │   └── 📄 schema.py                    # Request/Response message schemas
│   │   ├── 📁 swagger/                         # API documentation configuration
│   │   │   ├── 📄 swagger_config.py            # Swagger configuration settings
│   │   │   ├── 📄 swagger_docs.py              # API endpoint documentation
│   │   │   └── 📄 swagger_setup.py             # Swagger schema setup and initialization
│   │   └── 📁 utils/                           # Application utilities and helpers
│   │       ├── 📄 extension.py                 # Flask extensions (CORS, rate limiting..)
│   │       └── 📄 helpers.py                   # Application helper functions
│   ├── 📁 dotenv/                              # Environment configuration
│   │   ├── 📄 __init__.py                      # Dotenv package initialization
│   │   └── 📄 params.env                       # Environment variables configuration
│   └── 📁 logic/                               # Business logic layer
│       ├── 📄 document_query_get_process.py    # Main processing logic
│       └── 📁 utils/                           # Logic utilities
│           ├── 📁 config/                      # Configuration management
│           │   ├── 📄 config.py                # Configuration loader
│           │   ├── 📄 config.toml              # Configuration file
│           │   ├── 📄 gcp_client.py            # GCP client factory
│           │   └── 📄 secret_manager.py        # Secret Manager utilities
│           ├── 📁 GCS/                         # Google Cloud Storage utilities
│           │   ├── 📄 GcsUtils.py              # GCS operations
│           │   └── 📄 custom_errors.py         # GCS custom exceptions
│           ├── 📄 accounts_db.py               # AccountsDB query utilities
│           ├── 📄 documents_query_jobs.py      # DocumentsQueryJobs query utilities
│           ├── 📄 preprocessing.py            # Document preprocessing utilities
│           └── 📄 convertion_funcs.py          # Document conversion utilities
└── 📁 data/                                    # Data storage directory
    └── 📄 README.md                            # Data directory documentation
```

## 🗂️ Folder and File Descriptions

### Root Level
- **`main.py`**: Flask application entry point, configuration, and Google Cloud Functions integration
- **`requirements.txt`**: Python package dependencies and versions
- **`main.ipynb`**: Jupyter notebook for development, testing, and experimentation

### Application Layer (`app/application/`)
- **`document_query_get.py`**: Main API endpoint handler for document query get requests
- **`errors/`**: Error handling system
  - **`errors_class.py`**: Custom API error classes, exception handlers, and error formatting
  - **`errors_helpers.py`**: Error response generation for Swagger documentation
  - **`errors_mapping.py`**: Mapping between HTTP status codes and error classes
- **`mock/`**: Mock processing implementation
  - **`mock_process.py`**: Mock document query get logic for development and testing
- **`schemas/`**: Data validation and serialization
  - **`schema.py`**: Pydantic models for request/response validation and serialization
- **`swagger/`**: API documentation system
  - **`swagger_config.py`**: Swagger UI configuration and OpenAPI settings
  - **`swagger_docs.py`**: API endpoint documentation and examples
  - **`swagger_setup.py`**: Swagger schema registration and component setup
- **`utils/`**: Application-level utilities
  - **`extension.py`**: Flask extensions setup (CORS, rate limiting, Swagger, error handling)
  - **`helpers.py`**: Application helper functions for validation and processing

### Logic Layer (`app/logic/`)
- **`document_query_get_process.py`**: Main processing logic orchestrating all operations
- **`utils/`**: Business logic utilities
  - **`config/`**: Configuration management (TOML config, GCP clients, secrets)
  - **`GCS/`**: Google Cloud Storage operations
  - **`accounts_db.py`**: Firestore queries for client validation
  - **`documents_query_jobs.py`**: Firestore queries for retrieving query responses
  - **`preprocessing.py`**: Document preprocessing utilities
  - **`convertion_funcs.py`**: Document conversion utilities

### Configuration Layer (`app/dotenv/`)
- **`params.env`**: Environment variables for configuration (GCP settings, API limits, etc.)


## Getting Started

### Prerequisites
- Python 3.11+
- Google Cloud Platform account (for production use)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DocumentQueryGet
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud authentication**
   ```bash
   # Authenticate with Google Cloud
   gcloud auth login
   
   # Set your project ID
   gcloud config set project PROJECT_ID
   ```
   
   ***Note: This step is only required when running in real mode to ensure you are authenticated with the correct Google Cloud account and project. No code changes are needed - this is done entirely from your terminal.***

4. **Run the application**
   ```bash
   python -m main
   ```

The application will start on `http://localhost:8000` by default.

## Usage

### Processing Mode

DocumentQueryGet currently uses mock processing for development and testing. The mock implementation always returns success responses with sample data and can be easily replaced with real processing logic when needed.

### API Endpoints

- **Root**: `GET /` - Health check and status
- **Poll Threshold Check Result**: `POST /PollThresholdCheckResult` - Main document query get endpoint
- **API Documentation**: `GET /apidocs/` - Interactive Swagger documentation

### Example Request

```bash
curl -X POST "http://localhost:8000/shomer-saf/QueryGet/PollThresholdCheckResult" \
  -H "x-client-id: your-client-id" \
  -H "x-scope: your-scope" \
  -H "Content-Type: application/json" \
  -d '{
    "ClientRequestId": "123456789-304050_0001_20250311_1240"
  }'
```

### Response Format

The API returns query results with the following structure:

```json
{
  "RequestErrorCode": 200,
  "RequestErrorMessage": "OK",
  "QueriesPageResults": [
    {"queryID": "1", "page": "1", "response": "model response", "compliance": "True", "confidence": "0.9"}
  ],
  "QueriesResults": [
    {"queryID": "1", "compliance": "True"}
  ],
  "QueriesAggregatedResults": {
    "total_queries": 5,
    "true_queries": 2,
    "false_queries": 3
  }
}
```

### Key Features

#### Query Result Retrieval
- **Client Request ID**: Unique identifier for tracking processing jobs
- **Account Validation**: Validates client and scope via AccountsDB
- **Query Retrieval**: Queries DocumentsQueryJobs for query responses
- **Response Aggregation**: Aggregates query responses across multiple pages
- **Result Statistics**: Provides comprehensive query result statistics
- **Status Tracking**: Returns processing status and error information

#### Error Handling
- **Comprehensive Error Management**: Handles various error scenarios
- **Error Reporting**: Detailed error reporting and Cloud Logging
- **Status Codes**: Standardized HTTP status codes (200, 422, 500) for different scenarios
- **Error Messages**: Specific error messages (ACCOUNTS_DB_TIMEOUT, UNKNOWN_CLIENT, DB_TIMEOUT, NO_CONTENT, INTERNAL_ERROR)

## API Documentation

Once the application is running, visit `http://localhost:8000/apidocs/` to access the interactive Swagger documentation. The documentation includes:

- Complete API specification
- Request/response schemas
- Example requests and responses
- Error code documentation
- Interactive testing interface

### Environment Configuration
All configuration is managed through environment variables in `app/dotenv/params.env`:
- GCP project settings
- API rate limiting
- CORS configuration
- Swagger settings
- Processing timeouts

## 📄 License

This project is proprietary software. All rights reserved.

---

**DocumentQueryGet**

