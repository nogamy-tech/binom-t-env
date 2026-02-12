# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from datetime import datetime
from typing import List, Dict, Optional, Literal

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
from pydantic import BaseModel, Field

class BaseMessage(BaseModel):
    model_config = {"strict": False, "extra": "forbid"}
    RequestId: str = Field(..., description="Unique request reference, e.g., 'REQ_123456789'")
    Timestamp: datetime = Field(..., description="ISO 8601 timestamp, e.g., '2025-05-04T10:05:03.000'")
    Version: str = Field(..., description="Module version, e.g., 'app_v1.0.0'")
    Duration: Optional[int] = Field(None, description="Span duration in milliseconds")
    Status: Optional[Literal["SUCCESS", "PARTIAL_SUCCESS", "ERROR", "PENDING"]] = Field(
        None, description="Result status of the whole process. Use None to explicitly indicate no status"
    )


class PageProcessingRequest(BaseMessage):
    PageNumber: int = Field(..., description="Page number", example=1)
    Model: str = Field(..., description="The type of data extraction (text\\image) for page", example="Text")
    DnaTransactionId: str = Field(..., description="The unique request identifier", example="Shikun_syua-bediyur_123456789-304050_0001_20250311_1240")
    PagesBucketFolder: str = Field(..., description="Pages bucket folder path", example="gs://pages-bucket")
    DataBucketFolder: str = Field(..., description="Data bucket folder path", example="gs://data-bucket")
    BucketSubPath: str = Field(..., description="Bucket sub path", example="documents/processed")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "RequestId": "REQ_123456789",
                "Timestamp": "2025-01-15T10:30:00.000Z",
                "Version": "app_v1.0.0",
                "Duration": None,
                "Status": None,
                "PageNumber": 1,
                "Model": "Text",
                "DnaTransactionId": "Shikun_syua-bediyur_123456789-304050_0001_20250311_1240",
                "PagesBucketFolder": "gs://pages-bucket",
                "DataBucketFolder": "gs://data-bucket",
                "BucketSubPath": "documents/processed"
            }
        }
    }


class PageProcessingResponse(BaseModel):
    RequestErrorCode: int = Field(..., description="The request HTTP error code for the specific response", example=200)
    RequestErrorMessage: str = Field(..., description="The request HTTP error message for the specific response", example="SUCCESS")
    Path:str

    model_config = {
        "json_schema_extra": {
            "example": {
                "RequestErrorCode": 202,
                "RequestErrorMessage": "OK"
            }
        }
    }