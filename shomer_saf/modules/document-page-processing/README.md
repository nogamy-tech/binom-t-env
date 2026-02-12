# DocumentPageProcessing

A document page processing API built with Flask that splits documents into individual pages for processing. DocumentPageProcessing handles document chunking and page extraction, converting multi-page documents into individual page files for further processing.

## Description

DocumentPageProcessing is designed to split uploaded documents into individual pages for processing. It accepts document transaction IDs and processes them to create individual page files that can be used for subsequent document analysis and processing tasks. The service is built separating concerns into application, logic, and shared layers.

### Key Features
- **Document Chunking**: Splits multi-page documents into individual pages
- **Page Extraction**: Extracts individual pages from various document formats
- **Transaction Management**: Handles document transaction ID tracking
- **API Documentation**: Built-in Swagger/OpenAPI documentation
- **Error Handling**: Comprehensive error management and reporting
- **Mock Mode**: Switching between real and mock processing for development

## 📁 Project Structure

```
DocumentPageProcessing/
├── 📄 main.py                          # Application entry point and Flask app configuration
├── 📄 requirements.txt                 # Python dependencies
├── 📄 main.ipynb                       # Jupyter notebook for development/testing
├── 📁 app/                             # Main application package
│   ├── 📁 application/                 # Application layer (API, routes, schemas)
│   │   ├── 📄 page_chunker_job.py      # Main API endpoint and request handling
│   │   ├── 📁 errors/                  # Error handling and custom exceptions
│   │   │   ├── 📄 errors_class.py      # Custom API error classes and handlers
│   │   │   ├── 📄 errors_helpers.py    # Error response generation utilities
│   │   │   └── 📄 errors_mapping.py    # Error code to exception mapping
│   │   ├── 📁 schemas/                 # Pydantic data models and validation
│   │   │   └── 📄 schema.py            # Request/Response message schemas
│   │   ├── 📁 swagger/                 # API documentation configuration
│   │   │   ├── 📄 swagger_config.py    # Swagger configuration settings
│   │   │   ├── 📄 swagger_docs.py      # API endpoint documentation
│   │   │   └── 📄 swagger_setup.py     # Swagger schema setup and initialization
│   │   └── 📁 utils/                   # Application utilities and helpers
│   │       ├── 📄 extension.py         # Flask extensions (CORS, rate limiting..)
│   │       └── 📄 helpers.py           # Application helper functions
│   ├── 📁 dotenv/                      # Environment configuration
│   │   ├── 📄 __init__.py              # Dotenv package initialization
│   │   └── 📄 params.env               # Environment variables configuration
│   └── 📁 logic/                       # Business logic layer
│       ├── 📄 page_chunker_process.py  # Main document page chunking logic
│       ├── 📄 mock_process.py          # Mock implementation for testing
│       └── 📁 utils/                   # Logic utilities and helpers
│           └── 📄 helpers.py           # Logic helper functions and validators
└── 📁 data/                            # Data storage directory
    └── 📄 README.md                    # Data directory documentation
```

## 🗂️ Folder and File Descriptions

### Root Level
- **`main.py`**: Flask application entry point, configuration, and Google Cloud Functions integration
- **`requirements.txt`**: Python package dependencies and versions
- **`main.ipynb`**: Jupyter notebook for development, testing, and experimentation

### Application Layer (`app/application/`)
- **`page_chunker_job.py`**: Main API endpoint handler for document page chunking requests
- **`errors/`**: Error handling system
  - **`errors_class.py`**: Custom API error classes, exception handlers, and error formatting
  - **`errors_helpers.py`**: Error response generation for Swagger documentation
  - **`errors_mapping.py`**: Mapping between HTTP status codes and error classes
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

### Logic Layer (`app/logic/`)
- **`page_chunker_process.py`**: Core document page chunking pipeline for splitting documents
- **`mock_process.py`**: Mock implementation for development and testing without external dependencies
- **`utils/`**: Business logic utilities
  - **`helpers.py`**: Query validation, processing helpers, and utility functions


## Getting Started

### Prerequisites
- Python 3.11+
- Google Cloud Platform account (for production use)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DocumentPageProcessing
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

### Switching Between Logic Modes

DocumentPageProcessing supports two processing modes that can be easily switched by commenting/uncommenting lines in `main.py`:

#### Mock Mode (Development/Testing)
```python
# In main.py lines 53-54
logic = PageChunkerMockProcess()  # Mock logic - always returns success
#logic = PageChunkerProcess()     # Real logic - uses actual page chunking
```

#### Real Mode (Production)
```python
# In main.py lines 53-54
#logic = PageChunkerMockProcess()  # Mock logic - always returns success
logic = PageChunkerProcess()        # Real logic - uses actual page chunking
```

### API Endpoints

- **Root**: `GET /` - Health check and status
- **Document Page Chunker**: `POST /Document/PageChunker` - Main document page chunking endpoint
- **API Documentation**: `GET /apidocs/` - Interactive Swagger documentation

### Example Request

```bash
curl -X POST "http://localhost:8000/Document/PageChunker" \
  -H "Content-Type: application/json" \
  -d '{
  "RequestId": "REQ_123456789",
  "Timestamp": "2025-01-13T18:22:45.000Z",
  "Version": "app_v1.0.0",
  "DnaTransactionId": "Shikun_syua-bediyur_123456789-304050_0001_20250311_1240"
}'
```

### Response Format

The API returns processing status with the following structure:

```json
{
  "RequestErrorCode": 202,
  "RequestErrorMessage": "OK"
}
```


#### Error Handling
- **Timeout Handling**: Manages processing timeouts gracefully
- **Error Reporting**: Comprehensive error reporting and logging
- **Status Codes**: Standardized HTTP status codes for different scenarios

## API Documentation

Once the application is running, visit `http://localhost:8000/apidocs/` to access the interactive Swagger documentation. The documentation includes:

- Complete API specification
- Request/response schemas
- Example requests and responses
- Error code documentation

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

**DocumentPageProcessing**