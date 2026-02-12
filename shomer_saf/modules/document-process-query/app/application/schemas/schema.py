# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from datetime import datetime
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

    
class QueryItem(BaseModel):
    query: str  # The actual query string
    model: str  # The model type (e.g., text, image, etc.)
    id: str  # The ID, which can be either a string or an integer

    class Config:
        json_schema_extra = {
            "example": {
                "query": "some query",
                "model": "text",
                "id": "1"
            }
        }


class DocumentProcessRequest(BaseMessage):
    DnaTransactionId: str = Field(..., description="Unique request identifier")
    PageNumber: str = Field(..., description="Page number")
    Query: QueryItem = Field(..., description="Extraction type: text or image")
    DataBucketFolder: str = Field(..., description="Data bucket folder path")
    BucketSubPath: str = Field(..., description="Bucket sub path")

    class Config:
        json_schema_extra = {
            "example": {
                "RequestId": "REQ_123456789",
                "Timestamp": "2025-01-13T18:22:45.000Z",
                "Version": "app_v1.0.0",
                "DnaTransactionId": "Shikun_syua-bediyur_123456789-304050_0001_20250311_1240",
                "PageNumber": "1",
                "Query": {
                    "id": "1",
                    "model": "text",
                    "query": "some query"
                },
                "DataBucketFolder": "gs://data-bucket",
                "BucketSubPath": "documents/processed"
            }
        }


class DocumentProcessResponse(BaseModel):
    RequestErrorCode: int
    RequestErrorMessage: str
    LLMResponse:dict