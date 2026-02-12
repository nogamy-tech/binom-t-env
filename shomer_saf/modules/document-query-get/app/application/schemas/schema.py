# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from typing import List, Dict, Optional, Union
from typing_extensions import Literal

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
from pydantic import BaseModel, Field


class QueryPageResult(BaseModel):
    queryID: str = Field(..., title="Query ID", description="The query ID")
    page: str = Field(..., title="Page Number", description="The page number")
    response: str = Field(..., title="Model Response", description="Model response")
    compliance: str = Field(
        ..., title="Compliance", description="Compliance result (True/False)"
    )
    confidence: str = Field(
        ..., title="Confidence Score", description="Confidence score"
    )

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://nogamy.tech/schemas/query-page-result.json",
            "title": "Query Page Result Schema",
            "example": {
                "queryID": "1",
                "page": "1",
                "response": "model response",
                "compliance": "True",
                "confidence": "0.9",
            },
        },
    }


class QueryResult(BaseModel):
    queryID: str = Field(..., title="Query ID", description="The query ID")
    compliance: str = Field(
        ..., title="Compliance", description="Compliance result (True/False)"
    )

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://nogamy.tech/schemas/query-result.json",
            "title": "Query Result Schema",
            "example": {"queryID": "1", "compliance": "True"},
        },
    }


class QueriesAggregatedResults(BaseModel):
    total_queries: int = Field(
        ..., title="Total Queries", description="Total number of queries"
    )
    true_queries: int = Field(
        ..., title="True Queries", description="Number of queries with compliance True"
    )
    false_queries: int = Field(
        ...,
        title="False Queries",
        description="Number of queries with compliance False",
    )

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://nogamy.tech/schemas/queries-aggregated-results.json",
            "title": "Queries Aggregated Results Schema",
            "example": {"total_queries": 5, "true_queries": 2, "false_queries": 3},
        },
    }


class PollThresholdCheckResultRequest(BaseModel):
    ClientRequestId: str = Field(
        ...,
        title="Client Request ID",
        description="The Request Id from the client",
        pattern=r"^[A-Za-z0-9_\-]+$",
        examples=["123456789-304050_0001_20250311_1240"],
    )

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://nogamy.tech/schemas/poll-threshold-check-result-request.json",
            "title": "Poll Threshold Check Result Request Schema",
            "example": {"ClientRequestId": "123456789-304050_0001_20250311_1240"},
        },
    }


class PollThresholdCheckResultResponse(BaseModel):
    RequestErrorCode: int = Field(
        ...,
        title="Request Error Code",
        description="The request HTTP error code",
        examples=[200, 202, 204, 422, 424, 425, 460, 500],
    )
    RequestErrorMessage: Optional[str] = Field(
        None,
        title="Request Error Message",
        description="The request error message",
        examples=[
            "OK",
            "Unprocessable Entity",
            "ACCOUNTS_DB_TIMEOUT",
            "UNKNOWN_CLIENT",
            "DB_TIMEOUT",
            "NO_CONTENT",
            "INTERNAL_ERROR",
        ],
    )
    QueriesPageResults: Optional[List[Dict[str, str]]] = Field(
        None,
        title="Queries Page Results",
        description="The results to each query by page",
    )
    QueriesResults: Optional[List[Dict[str, str]]] = Field(
        None,
        title="Queries Results",
        description="The results to each query aggregated across all pages",
    )
    QueriesAggregatedResults: Optional[Dict[str, int]] = Field(
        None,
        title="Queries Aggregated Results",
        description="The results to all queries aggregated together",
    )

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://nogamy.tech/schemas/poll-threshold-check-result-response.json",
            "title": "Poll Threshold Check Result Response Schema",
            "example": {
                "RequestErrorCode": 200,
                "RequestErrorMessage": "OK",
                "QueriesPageResults": [
                    {
                        "queryID": "1",
                        "page": "1",
                        "response": "model response",
                        "compliance": "True",
                        "confidence": "0.9",
                    }
                ],
                "QueriesResults": [{"queryID": "1", "compliance": "True"}],
                "QueriesAggregatedResults": {
                    "total_queries": 5,
                    "true_queries": 2,
                    "false_queries": 3,
                },
            },
        },
    }
