"""
Utilities for triggering Google Cloud Workflows.
"""
from datetime import datetime
import json
from typing import Dict, List
from google.cloud.workflows import executions_v1
from google.cloud.workflows.executions_v1.types import Execution
from google.api_core.exceptions import DeadlineExceeded, GoogleAPIError

from app.logic.utils.services.gcp_client import GCPServiceFactory


class WorkflowTimeout(Exception):
    """Raised when a workflow operation times out."""

    pass


class WorkflowError(Exception):
    """Raised when a workflow returns an error."""

    pass


class Workflow:
    """A class to manage Google Cloud Workflow executions."""

    def __init__(self, gcp_service_factory: GCPServiceFactory, project_id: str, region: str):
        """
        Initializes the Workflow client.

        Args:
            gcp_service_factory: An instance of GCPServiceFactory.
            project_id: The GCP project ID.
            region: The GCP location/region.
        """
        self.project_id = project_id
        self.region = region
        self.executions_client = gcp_service_factory.get_gcp_client("workflow_executions")

    def _list_running_executions(self, workflow_name: str) -> List[Execution]:
        """Lists all running executions for a given workflow."""
        parent = f"projects/{self.project_id}/locations/{self.region}/workflows/{workflow_name}"
        list_executions_request = executions_v1.ListExecutionsRequest(parent=parent, view=executions_v1.ExecutionView.FULL)
        running_states = [Execution.State.ACTIVE, Execution.State.QUEUED]

        running_executions = []
        for execution in self.executions_client.list_executions(request=list_executions_request):
            if execution.state in running_states:
                running_executions.append(execution)
        return running_executions

    def _filter_executions_by_argument(self, executions: List[Execution], key: str, value: str) -> List[Execution]:
        """Filters a list of executions by a specific argument key-value pair."""
        filtered_executions = []
        for execution in executions:
            try:
                args = json.loads(execution.argument)
                if args.get(key) == value:
                    filtered_executions.append(execution)
            except (json.JSONDecodeError, AttributeError):
                continue
        return filtered_executions

    def check_workflow_running(self, workflow_name: str, filter_key: str, filter_value: str) -> bool:
        """
        Check if a workflow with a specific argument is currently running.

        Args:
            workflow_name: The workflow name/path.
            filter_key: The argument key to filter by.
            filter_value: The argument value to match.

        Returns:
            bool: True if a matching workflow is running, False otherwise.
        """
        try:
            running_executions = self._list_running_executions(workflow_name)
            matching_executions = self._filter_executions_by_argument(running_executions, filter_key, filter_value)
            return bool(matching_executions)
        except Exception as e:
            print(f"Warning: Could not check workflow status: {e}")
            return False

    def trigger_workflow(
        self,
        workflow_name: str,
        dna_transaction_id: str,
        page_count: int,
        queries: List[Dict[str, str]],
        query_ids: List[str],
        documents_bucket_folder: str,
        pages_bucket_folder: str,
        data_bucket_folder: str,
        bucket_sub_path: str,
        RequestId:str,
        Timestamp:datetime,
        Version:str,
    ) -> None:
        """
        Trigger a Google Cloud Workflow with the given parameters.

        Args:
            workflow_name: The workflow name/path.
            dna_transaction_id: The DnaTransactionId.
            page_count: Number of pages in the document.
            queries: List of queries with their types.
            query_ids: List of QueryIds.
            documents_bucket_folder: Documents bucket folder.
            pages_bucket_folder: Pages bucket folder.
            data_bucket_folder: Data bucket folder.
            bucket_sub_path: Bucket sub path.
            RequestId: RequestId.
            Timestamp: Timestamp.
            Version: Version.

        Raises:
            WorkflowTimeout: If the workflow trigger times out.
            WorkflowError: If the workflow returns an error.
        """
        try:
            execution_arg = {
                "DnaTransactionId": dna_transaction_id,
                "PageCount": page_count,
                "Queries": queries,
                "QueryIds": query_ids,
                "DocumentsBucketFolder": documents_bucket_folder,
                "PagesBucketFolder": pages_bucket_folder,
                "DataBucketFolder": data_bucket_folder,
                "BucketSubPath": bucket_sub_path,
                "RequestId": RequestId,
                "Timestamp": Timestamp,
                "Version": Version,
            }

            parent = f"projects/{self.project_id}/locations/{self.region}/workflows/{workflow_name}"

            request = executions_v1.CreateExecutionRequest(parent=parent, execution=Execution(argument=json.dumps(execution_arg)))

            execution = self.executions_client.create_execution(request=request, timeout=30)

            if execution.state == Execution.State.FAILED:
                raise WorkflowError(f"Workflow execution failed: {execution.error}")

        except DeadlineExceeded:
            raise WorkflowTimeout(f"Workflow trigger timed out for {dna_transaction_id}")
        except GoogleAPIError as e:
            if "deadline" in str(e).lower() or "timeout" in str(e).lower():
                raise WorkflowTimeout(f"Workflow trigger timed out: {e}")
            raise WorkflowError(f"Workflow API error: {e}")
        except Exception as e:
            error_msg = str(e).lower()
            if "deadline" in error_msg or "timeout" in error_msg:
                raise WorkflowTimeout(f"Workflow trigger timed out: {e}")
            elif "failed" in error_msg or "error" in error_msg:
                raise WorkflowError(f"Workflow error: {e}")
            else:
                raise WorkflowError(f"Unexpected workflow error: {e}")
