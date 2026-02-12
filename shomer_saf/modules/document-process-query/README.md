# DocumentProcessQuery

A document query processing API built with Flask that processes document queries using Google Cloud. DocumentProcessQuery can handle text and image-based queries on specific document pages, providing responses through Vertex AI integration.

## Description

DocumentProcessQuery is designed to process user queries against specific document pages using Google Cloud Vertex AI models. It accepts document transaction IDs, page numbers, and queries, then returns intelligent responses based on the document content. The service is built separating concerns into application, logic, and shared layers.

### Key Features
- **Multi-Model Support**: Handles both text and image-based queries
- **Document Page Processing**: Queries specific pages of documents using transaction IDs
- **Vertex AI Integration**: Uses Google Cloud Vertex AI for intelligent query processing
- **Performance**: Optimized for fast document query processing
- **API Documentation**: Built-in Swagger/OpenAPI documentation
- **Error Handling**: Comprehensive error management and reporting
- **Mock Mode**: Switching between real and mock processing for development

## 📁 Project Structure

```
DocumentProcessQuery/
├── 📄 main.py                          # Application entry point and Flask app configuration
├── 📄 requirements.txt                 # Python dependencies
├── 📄 main.ipynb                       # Jupyter notebook for development/testing
├── 📁 app/                             # Main application package
│   ├── 📁 application/                 # Application layer (API, routes, schemas)
│   │   ├── 📄 document_process_query_job.py # Main API endpoint and request handling
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
│       ├── 📄 document_process_query.py # Main document query processing logic
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
- **`document_process_query_job.py`**: Main API endpoint handler for document query processing requests
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
- **`document_process_query.py`**: Core document query processing pipeline with Google Cloud Vertex AI integration
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
   cd DocumentProcessQuery
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

DocumentProcessQuery supports two processing modes that can be easily switched by commenting/uncommenting lines in `main.py`:

#### Mock Mode (Development/Testing)
```python
# In main.py lines 53-54
logic = DocumentMockProcess()  # Mock logic - always returns success
#logic = DocumentProcess()     # Real logic - uses Google Cloud Vertex AI
```

#### Real Mode (Production)
```python
# In main.py lines 53-54
#logic = DocumentMockProcess()  # Mock logic - always returns success
logic = DocumentProcess()        # Real logic - uses Google Cloud Vertex AI
```

### API Endpoints

- **Root**: `GET /` - Health check and status
- **Document Query Processing**: `POST /Document/ProcessQuery` - Main document query processing endpoint
- **API Documentation**: `GET /apidocs/` - Interactive Swagger documentation

### Example Request

```bash
curl -X POST "http://localhost:8000/Document/ProcessQuery" \
  -H "Content-Type: application/json" \
  -d '{
  "RequestId": "REQ_123456789",
  "Timestamp": "2025-01-13T18:22:45.000Z",
  "Version": "app_v1.0.0",
  "DnaTransactionId": "Shikun_syua-bediyur_123456789-304050_0001_20250311_1240",
  "PageNumber": 1,
  "Query": {
    "id": "1",
    "model": "text",
    "query": "What is the main topic of this document?"
  }
}'
```

### Query Types

The API supports two types of queries:

#### Text Queries
- **Model**: `"text"`
- **Use Case**: Natural language questions about document content
- **Example**: `"What is the main topic of this document?"`

#### Image Queries
- **Model**: `"image"`
- **Use Case**: Visual analysis and image-based questions
- **Example**: `"What charts or graphs are shown in this page?"`

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

**DocumentProcessQuery**