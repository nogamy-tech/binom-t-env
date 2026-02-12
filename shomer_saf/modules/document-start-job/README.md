# DocumentStartJob

A document start job API built with Flask that handles document processing initiation with queue threshold checks. DocumentStartJob validates input, checks accounts, validates documents, saves to buckets, creates DB records, and triggers workflows for document processing.

## Description

DocumentStartJob is designed to handle the initial phase of document processing workflows. It accepts document files, client requests, and queries, validates them, saves documents to cloud storage, creates tracking records, and triggers asynchronous processing workflows. The service is built with a clean application layer architecture using mock processing for development and testing.

### Key Features
- **Document Validation**: Validates document format (PDF, JPEG, PNG) and integrity
- **Account Management**: Queries AccountsDB to validate client and scope
- **Bucket Management**: Manages document bucket operations and folder structure
- **Database Records**: Creates and manages DocumentQueryResponse records
- **Workflow Integration**: Triggers Google Cloud Workflows for asynchronous processing
- **API Documentation**: Built-in Swagger/OpenAPI documentation
- **Error Handling**: Comprehensive error management and reporting
- **Mock Processing**: Mock implementation for development and testing

## 📁 Project Structure

```
DocumentStartJob/
├── 📄 .gcloudignore
├── 📄 .gitignore
├── 📄 DEPLOY.md
├── 📄 main.ipynb
├── 📄 main.py
├── 📄 README.md
├── 📄 requirements.txt
├── 📁 app/
│   ├── 📄 __init__.py
│   ├── 📁 application/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 document_start_job.py
│   │   ├── 📁 errors/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 errors_class.py
│   │   │   ├── 📄 errors_helpers.py
│   │   │   └── 📄 errors_mapping.py
│   │   ├── 📁 mock/
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 mock_process.py
│   │   ├── 📁 schemas/
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 schema.py
│   │   ├── 📁 swagger/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 swagger_config.py
│   │   │   ├── 📄 swagger_docs.py
│   │   │   └── 📄 swagger_setup.py
│   │   └── 📁 utils/
│   │       ├── 📄 __init__.py
│   │       ├── 📄 extension.py
│   │       └── 📄 helpers.py
│   ├── 📁 dotenv/
│   │   ├── 📄 __init__.py
│   │   └── 📄 params.env
│   └── 📁 logic/
│       ├── 📄 __init__.py
│       ├── 📄 document_start_job_process.py
│       └── 📁 utils/
│           ├── 📄 __init__.py
│           ├── 📄 accounts_db.py
│           ├── 📄 document_query_response.py
│           ├── 📄 document_validation.py
│           ├── 📄 logging.py
│           ├── 📄 workflow.py
│           ├── 📁 config/
│           │   ├── 📄 __init__.py
│           │   ├── 📄 base_prompt.txt
│           │   ├── 📄 config.py
│           │   ├── 📄 config.toml
│           │   ├── 📄 gcp_client.py
│           │   └── 📄 secret_manager.py
│           ├── 📁 Firestore/
│           │   ├── 📄 __init__.py
│           │   └── 📄 firestore.py
│           └── 📁 GCS/
│               ├── 📄 __init__.py
│               ├── 📄 custom_errors.py
│               └── 📄 GcsUtils.py
├── 📁 data/
│   ├── 📄 README.md
│   └── 📄 shay_test_payslip.pdf
└── 📁 tests/
    ├── 📄 encode_base64.ipynb
    ├── 📄 encode_base64.py
    ├── 📄 test_blobs.ipynb
    ├── 📄 test_pipe.py
    └── 📄 test_workflow.ipynb
```

## 🗂️ Folder and File Descriptions

### Root Level
- **`.gcloudignore`**: Specifies files to be ignored by the gcloud command-line tool.
- **`.gitignore`**: Specifies intentionally untracked files to be ignored by Git.
- **`DEPLOY.md`**: Instructions and notes for deploying the application.
- **`main.py`**: Flask application entry point and configuration.
- **`main.ipynb`**: Jupyter notebook for development and testing.
- **`README.md`**: This file, providing an overview of the project.
- **`requirements.txt`**: A list of the Python packages that the project depends on.

### `app` Directory
- **`application/`**: Contains the application layer, which includes the API, routes, and schemas.
  - **`document_start_job.py`**: The main API endpoint and request handling logic.
  - **`errors/`**: Handles errors and custom exceptions.
    - **`errors_class.py`**: Defines custom API error classes.
    - **`errors_helpers.py`**: Utility functions for generating error responses.
    - **`errors_mapping.py`**: Maps error codes to specific exceptions.
  - **`mock/`**: Holds the mock processing implementation.
    - **`mock_process.py`**: Provides mock logic for the document start job.
  - **`schemas/`**: Contains Pydantic data models for validation.
    - **`schema.py`**: Defines the schemas for request and response messages.
  - **`swagger/`**: Manages API documentation.
    - **`swagger_config.py`**: Configuration settings for Swagger.
    - **`swagger_docs.py`**: Documentation for the API endpoints.
    - **`swagger_setup.py`**: Sets up the Swagger schema.
  - **`utils/`**: Contains application-level utilities.
    - **`extension.py`**: Manages Flask extensions like CORS and rate limiting.
    - **`helpers.py`**: Provides helper functions for the application.
- **`dotenv/`**: Manages environment configuration.
  - **`params.env`**: Stores environment variables.
- **`logic/`**: The business logic layer of the application.
  - **`document_start_job_process.py`**: The main processing logic.
  - **`utils/`**: Contains utilities for the business logic.
    - **`accounts_db.py`**: Provides utilities for querying the accounts database.
    - **`document_query_response.py`**: Manages the response from document queries.
    - **`document_validation.py`**: Includes utilities for validating documents.
    - **`logging.py`**: Manages logging for the application.
    - **`workflow.py`**: Provides utilities for handling workflows.
    - **`config/`**: Manages configuration settings.
      - **`base_prompt.txt`**: A base prompt for language models.
      - **`config.py`**: The main configuration script.
      - **`config.toml`**: The configuration file in TOML format.
      - **`gcp_client.py`**: A factory for creating Google Cloud Platform clients.
      - **`secret_manager.py`**: Utilities for managing secrets.
    - **`Firestore/`**: Contains utilities for interacting with Firestore.
      - **`firestore.py`**: The main Firestore utility script.
    - **`GCS/`**: Includes utilities for Google Cloud Storage.
      - **`custom_errors.py`**: Defines custom errors for GCS operations.
      - **`GcsUtils.py`**: Provides utility functions for GCS.

### `data` Directory
- **`README.md`**: Documentation for the data directory.
- **`shay_test_payslip.pdf`**: A sample PDF file for testing.


## Getting Started

### Prerequisites
- Python 3.11+
- Google Cloud Platform account (for production use)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DocumentStartJob
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

DocumentStartJob currently uses mock processing for development and testing. The mock implementation always returns success responses and can be easily replaced with real processing logic when needed.

### API Endpoints

- **Root**: `GET /` - Health check and status
- **Queue Threshold Check**: `POST /QueueThresholdCheck` - Main document start job endpoint
- **API Documentation**: `GET /apidocs/` - Interactive Swagger documentation

### Example Request

```bash
curl -X POST "http://localhost:8000/shomer-saf/StartJob/QueueThresholdCheck" \
  -H "x-client-id: your-client-id" \
  -H "x-scope: your-scope" \
  -H "Content-Type: application/json" \
  -d '{
    "ClientRequestId": "123456789-304050_0001_20250311_1240",
    "Document": "base64encodeddocument==",
    "Queries": [
      {"query": "is the document signed", "model": "image"},
      {"query": "is it an engineering degree", "model": "text"}
    ]
  }'
```

### Response Format

The API returns processing results with the following structure:

```json
{
  "RequestErrorCode": 202,
  "RequestErrorMessage": "OK"
}
```

### Key Features

#### Document Processing Initiation
- **Client Request ID**: Unique identifier for tracking processing jobs
- **Document Validation**: Validates format (PDF, JPEG, PNG) and integrity
- **Account Validation**: Validates client and scope via AccountsDB
- **Bucket Management**: Handles document bucket operations and folder structure
- **Database Records**: Creates DocumentQueryResponse records for tracking
- **Workflow Triggering**: Asynchronously triggers Google Cloud Workflows
- **Status Tracking**: Returns processing status and error information

#### Error Handling
- **Comprehensive Error Management**: Handles various error scenarios
- **Error Reporting**: Detailed error reporting and Cloud Logging
- **Status Codes**: Standardized HTTP status codes (422, 500) for different scenarios
- **Error Messages**: Specific error messages (ACCOUNTS_DB_TIMEOUT, UNKNOWN_CLIENT, UNSUPPORTED_FORMAT, etc.)

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

**DocumentStartJob**

