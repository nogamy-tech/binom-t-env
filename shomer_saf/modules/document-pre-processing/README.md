# DocumentPreProcessing

A document pre-processing API built with Flask that handles document preprocessing with bucket management. DocumentPreProcessing processes documents with specified bucket paths and transaction IDs, providing preprocessing capabilities for document workflows.

## Description

DocumentPreProcessing is designed to handle document preprocessing tasks with bucket management. It accepts transaction IDs and bucket paths, processes documents, and returns preprocessing results. The service is built with a clean application layer architecture using mock processing for development and testing.

### Key Features
- **Document Preprocessing**: Processes documents with bucket path management
- **Transaction Tracking**: Handles unique transaction IDs for request tracking
- **Bucket Management**: Manages document and page bucket operations
- **API Documentation**: Built-in Swagger/OpenAPI documentation
- **Error Handling**: Comprehensive error management and reporting
- **Mock Processing**: Mock implementation for development and testing

## 📁 Project Structure

```
DocumentPreProcessing/
├── 📄 main.py                                  # Application entry point and Flask app configuration
├── 📄 requirements.txt                         # Python dependencies
├── 📄 main.ipynb                               # Jupyter notebook for development/testing
├── 📁 app/                                     # Main application package
│   ├── 📁 application/                         # Application layer (API, routes, schemas)
│   │   ├── 📄 document_pre_processing_job.py   # Main API endpoint and request handling
│   │   ├── 📁 errors/                          # Error handling and custom exceptions
│   │   │   ├── 📄 errors_class.py              # Custom API error classes and handlers
│   │   │   ├── 📄 errors_helpers.py            # Error response generation utilities
│   │   │   └── 📄 errors_mapping.py            # Error code to exception mapping
│   │   ├── 📁 mock/                            # Mock processing implementation
│   │   │   ├── 📄 __init__.py                  # Mock package initialization
│   │   │   └── 📄 mock_process.py              # Mock document preprocessing logic
│   │   ├── 📁 schemas/                         # Pydantic data models and validation
│   │   │   └── 📄 schema.py                    # Request/Response message schemas
│   │   ├── 📁 swagger/                         # API documentation configuration
│   │   │   ├── 📄 swagger_config.py            # Swagger configuration settings
│   │   │   ├── 📄 swagger_docs.py              # API endpoint documentation
│   │   │   └── 📄 swagger_setup.py             # Swagger schema setup and initialization
│   │   └── 📁 utils/                           # Application utilities and helpers
│   │       ├── 📄 extension.py                 # Flask extensions (CORS, rate limiting..)
│   │       └── 📄 helpers.py                   # Application helper functions
│   └── 📁 dotenv/                              # Environment configuration
│       ├── 📄 __init__.py                      # Dotenv package initialization
│       └── 📄 params.env                       # Environment variables configuration
└── 📁 data/                                    # Data storage directory
    └── 📄 README.md                            # Data directory documentation
```

## 🗂️ Folder and File Descriptions

### Root Level
- **`main.py`**: Flask application entry point, configuration, and Google Cloud Functions integration
- **`requirements.txt`**: Python package dependencies and versions
- **`main.ipynb`**: Jupyter notebook for development, testing, and experimentation

### Application Layer (`app/application/`)
- **`document_pre_processing_job.py`**: Main API endpoint handler for document pre-processing requests
- **`errors/`**: Error handling system
  - **`errors_class.py`**: Custom API error classes, exception handlers, and error formatting
  - **`errors_helpers.py`**: Error response generation for Swagger documentation
  - **`errors_mapping.py`**: Mapping between HTTP status codes and error classes
- **`mock/`**: Mock processing implementation
  - **`mock_process.py`**: Mock document preprocessing logic for development and testing
- **`schemas/`**: Data validation and serialization
  - **`schema.py`**: Pydantic models for request/response validation and serialization
- **`swagger/`**: API documentation system
  - **`swagger_config.py`**: Swagger UI configuration and OpenAPI settings
  - **`swagger_docs.py`**: API endpoint documentation and examples
  - **`swagger_setup.py`**: Swagger schema registration and component setup
- **`utils/`**: Application-level utilities
  - **`extension.py`**: Flask extensions setup (CORS, rate limiting, Swagger, error handling)
  - **`helpers.py`**: Application helper functions for validation and processing

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
   cd DocumentPreProcessing
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

DocumentPreProcessing currently uses mock processing for development and testing. The mock implementation always returns success responses and can be easily replaced with real processing logic when needed.

### API Endpoints

- **Root**: `GET /` - Health check and status
- **Document PreProcessing**: `POST /Document/PreProcessing` - Main document preprocessing endpoint
- **API Documentation**: `GET /apidocs/` - Interactive Swagger documentation

### Example Request

```bash
curl -X POST "http://localhost:8000/Document/PreProcessing" \
  -H "Content-Type: application/json" \
  -d '{
  "RequestId": "REQ_123456789",
  "Timestamp": "2023-07-23T12:34:56.789Z",
  "Version": "app_v1.0.0",
  "DnaTransactionId": "Shikun_syua-bediyur_123456789-304050_0001_20250311_1240",
  "DocumentsBucket": "documents-bucket",
  "Folder": "documents/folder",
  "PagesBucketFolder": "pages/folder",
  "BucketSubPath": "sub/path"
}'
```

### Response Format

The API returns preprocessing results with the following structure:

```json
{
  "RequestErrorCode": 200,
  "RequestErrorMessage": "SUCCESS"
}
```

### Key Features

#### Document Preprocessing
- **Transaction ID**: Unique identifier for tracking preprocessing jobs
- **Bucket Management**: Handles document and page bucket operations
- **Path Management**: Manages folder and sub-path configurations
- **Status Tracking**: Returns processing status and error information

#### Error Handling
- **Comprehensive Error Management**: Handles various error scenarios
- **Error Reporting**: Detailed error reporting and logging
- **Status Codes**: Standardized HTTP status codes for different scenarios

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

**DocumentPreProcessing**