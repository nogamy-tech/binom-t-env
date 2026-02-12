"""
Utilities for querying AccountsDB (Firestore) to get MinistryName and ProjectName.
"""

from typing import Tuple
from app.logic.utils.services.firestore import FirestoreClient
from google.api_core.exceptions import DeadlineExceeded, NotFound


class AccountsDBTimeout(Exception):
    """Raised when AccountsDB query times out"""

    pass


class UnknownClient(Exception):
    """Raised when client-id or scope not found in AccountsDB"""

    pass


def query_accounts_db(db_client: FirestoreClient, x_client_id: str, x_scope: str) -> Tuple[str, str]:
    """Queries AccountsDB to retrieve MinistryName and ProjectName.

    This function connects to the AccountsDB (Firestore) to fetch client-specific
    data based on the provided client ID and scope. It ensures that both the
    client and the scope are valid and retrieves the associated MinistryName and
    ProjectName.

    Args:
        db_client: An instance of the Firestore client, used to interact with the database.
        x_client_id: The identifier for the client making the request.
        x_scope: The scope of the request, used to identify the specific
            configuration for the client.

    Returns:
        A dictionary containing the document data for the specified client and scope.

    Raises:
        AccountsDBTimeout: If the database query exceeds the allowed time limit.
        UnknownClient: If the provided x_client_id or x_scope is not found in the database,
            or if MinistryName or ProjectName are missing for the given scope.
    """

    try:
        db_client.set_internal_id(f"{x_client_id}_{x_scope}")
        doc = db_client.get_document_from_db()

        try:
            if not doc:
                raise UnknownClient(f"Client '{x_client_id}' not found in AccountsDB")

            data = doc[0]

            # Check if scope exists in the client's scopes
            scopes = data.get("x-scope", {})
            if x_scope not in scopes:
                raise UnknownClient(f"Scope '{x_scope}' not found for client '{x_client_id}'")

            ministry_name = data.get("MinistryName")
            project_name = data.get("ProjectName")

            if not ministry_name or not project_name:
                raise UnknownClient(f"Missing MinistryName or ProjectName for client '{x_client_id}' with scope '{x_scope}'")

            return data

        except DeadlineExceeded:
            raise AccountsDBTimeout(f"AccountsDB query timed out for client '{x_client_id}'")
        except NotFound:
            raise UnknownClient(f"Client '{x_client_id}' or scope '{x_scope}' not found in AccountsDB")

    except AccountsDBTimeout:
        raise
    except UnknownClient:
        raise
    except Exception as e:
        # For any other error, treat as timeout for now
        if "deadline" in str(e).lower() or "timeout" in str(e).lower():
            raise AccountsDBTimeout(f"AccountsDB query timed out: {e}")
        raise UnknownClient(f"Error querying AccountsDB: {e}")
