
# Document Clear DB

A Google Cloud Function to clear documents and data from Google Cloud Storage and Firestore.

## Description

This project provides a Google Cloud Function that clears data from Google Cloud Storage buckets and a Firestore collection. The function is triggered by a Pub/Sub message containing a list of transaction IDs. If the list is empty, it clears all data older than a configured time.

### Key Features
- **Clear by Transaction ID**: Deletes specific documents and blobs corresponding to a list of transaction IDs.
- **Clear All**: Deletes all documents and blobs older than a specified time.
- **Google Cloud Integration**: Designed to run as a Google Cloud Function triggered by Pub/Sub.
- **Error Handling**: Handles errors related to bucket access, blob existence, and database failures.

## 📁 Project Structure

```
document-clear-db/
├── 📄 main.py                                  # Cloud Function entry point
├── 📄 requirements.txt                         # Python dependencies
├── 📁 app/                                     # Main application package
│   ├── 📁 config/                             # Configuration files
│   │   └── 📄 config.py                       # Configuration loading
│   ├── 📁 GCS/                                # Google Cloud Storage utilities
│   │   ├── 📄 GcsUtils.py                     # GCS helper functions
│   │   └── 📄 custom_errors.py                # Custom error classes for GCS
│   ├── 📁 Firestore/                          # Firestore utilities
│   │   └── 📄 firestore.py                    # Firestore helper functions
│   └── 📁 src/                                  # Source code
│       └── 📄 main_process.py                 # Main processing logic
└── 📁 data/                                    # Data storage directory
    └── 📄 README.md                            # Data directory documentation
```

## 🗂️ Folder and File Descriptions

### Root Level
- **`main.py`**: The entry point for the Google Cloud Function. It receives the Pub/Sub message and calls the main processing logic.
- **`requirements.txt`**: A list of the Python packages required for the project.

### Application (`app/`)
- **`config/`**: Handles configuration management.
- **`GCS/`**: Contains modules for interacting with Google Cloud Storage.
  - **`GcsUtils.py`**: Provides functions for deleting blobs and folders from GCS.
  - **`custom_errors.py`**: Defines custom exceptions for GCS operations.
- **`Firestore/`**: Contains modules for interacting with Firestore.
  - **`firestore.py`**: Provides functions for cleaning collections and deleting documents from Firestore.
- **`src/`**: Contains the main source code for the application.
  - **`main_process.py`**: The core logic for clearing the database and buckets.

## Getting Started

### Prerequisites
- Python 3.11+
- Google Cloud Platform account
- `gcloud` CLI installed and authenticated

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd document-clear-db
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud**
   This function is intended to be deployed on Google Cloud. You will need to set up a Pub/Sub topic and configure the necessary permissions for the function to access GCS and Firestore.

## Usage

This function is triggered by a message published to a Pub/Sub topic. The message must be a JSON object containing a key `"items"` with a list of strings as its value.

### Example Pub/Sub Message

To clear specific transactions:
```json
{
  "items": ["transaction_id_1", "transaction_id_2"]
}
```

To clear all old data:
```json
{
  "items": []
}
```

### Configuration

The project is configured through the `app/config/config.py` file. This file should be set up to load your project's specific configuration, such as bucket names, Firestore database and collection names, and time cutoffs for clearing data.

## 📄 License

This project is proprietary software. All rights reserved.
