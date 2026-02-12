# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from typing import List, Dict, Literal

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
from pydantic import BaseModel, Field


class QueryItem(BaseModel):
    query: str = Field(..., title="Query Text", description="The user query to answer")
    model: Literal["text", "image"] = Field(
        ..., title="Model Type", description="The type of query (text or image)"
    )

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://nogamy.tech/schemas/query-item.json",
            "title": "Query Item Schema",
            "example": {"query": "is the document signed", "model": "image"},
        },
    }


class QueueThresholdCheckRequest(BaseModel):
    ClientRequestId: str = Field(
        ...,
        title="Client Request ID",
        description="The client request identifier",
        pattern=r"^[A-Za-z0-9_\-]+$",
        examples=["123456789-304050_0001_20250311_1240"],
    )
    Document: str = Field(
        ..., title="Base64 Document", description="A base64 encoded document"
    )
    Queries: List[QueryItem] = Field(
        ...,
        title="Queries List",
        description="The user queries to answer and their type (text, image)",
    )

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://nogamy.tech/schemas/queue-threshold-check-request.json",
            "title": "Queue Threshold Check Request Schema",
            "example": {
                "ClientRequestId": "123456789-304050_0001_20250311_1240",
                "Document": "base64encodeddocument==",
                "Queries": [
                    {"query": "is the document signed", "model": "image"},
                    {"query": "is it an engineering degree", "model": "text"},
                ],
            },
        },
    }


class QueueThresholdCheckResponse(BaseModel):
    RequestErrorCode: int = Field(
        ...,
        title="Request Error Code",
        description="The request HTTP error code for the specific response",
        examples=[200, 422, 500],
    )
    RequestErrorMessage: str = Field(
        ...,
        title="Request Error Message",
        description="The request HTTP error message for the specific response",
        examples=["OK", "Unprocessable Entity", "Internal Server Error"],
    )

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://nogamy.tech/schemas/queue-threshold-check-response.json",
            "title": "Queue Threshold Check Response Schema",
            "example": {"RequestErrorCode": 200, "RequestErrorMessage": "OK"},
        },
    }
