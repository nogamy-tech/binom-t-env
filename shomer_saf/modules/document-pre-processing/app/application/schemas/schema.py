# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from datetime import datetime, timezone
from typing import Optional, Literal
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


class DocumentPreProcessingRequest(BaseMessage):
    DnaTransactionId: str = Field(..., description="The unique request identifier")
    DocumentsBucketFolder: str = Field(..., description="Documents bucket name")
    PagesBucketFolder: str = Field(..., description="Pages bucket folder path")
    BucketSubPath: str = Field(..., description="Bucket sub path")

    model_config = {
        "json_schema_extra": {
            "example": {
                    "RequestId": "REQ_123456789",
                    "Timestamp": "2025-01-27T10:05:03.000Z",
                    "Version": "app_v1.0.0",
                    "DnaTransactionId": "Shikun_syua-bediyur_123456789-304050_0001_20250311_1240",
                    "DocumentsBucketFolder": "documents-bucket",
                    "PagesBucketFolder": "pages/folder",
                    "BucketSubPath": "sub/path"
                    },
        }
    }


class DocumentPreProcessingResponse(BaseModel):
    RequestErrorCode: int = Field(..., description="The request HTTP error code for the specific response")
    RequestErrorMessage: str = Field(..., description="The request HTTP error message for the specific response")

    model_config = {
        "json_schema_extra": {
            "example": {
                "RequestErrorCode": 200,
                "RequestErrorMessage": "SUCCESS"
            },
        }
    }


