from google.oauth2 import service_account
from pathlib import Path
import json
from app.logic.utils.services.gcp_client import GCPServiceFactory

from concurrent.futures import ThreadPoolExecutor, as_completed


class SecretVault:
    def __init__(self, gcp_service_factory: GCPServiceFactory):
        """
        Initializes the SecretVault.

        This method sets up the Secret Manager client and determines the GCP project ID.
        It uses a GCPServiceFactory to create the necessary GCP clients. If no factory
        is provided, a default one is instantiated.

        Args:
            gcp_service_factory (GCPServiceFactory, optional): An instance of
                GCPServiceFactory for creating GCP clients. Defaults to None,
                which creates a new factory.
        """
        self.project_id = gcp_service_factory.get_projectid()
        self.client = gcp_service_factory.get_gcp_client("secret_manager")

    def _get_single_secret(self, secret_id: str) -> tuple[str, str]:
        """
        Fetches a single secret from GCP Secret Manager.

        Args:
            secret_id (str): The ID of the secret to retrieve.

        Returns:
            tuple[str, str]: A tuple containing the secret ID and its value.

        Raises:
            ValueError: If no enabled secret versions are found.
        """
        parent = self.client.secret_path(self.project_id, secret_id)
        versions = self.client.list_secret_versions(request={"parent": parent, "filter": 'state: "ENABLED"'})
        latest_enabled_version = next(iter(versions), None)

        if not latest_enabled_version:
            raise ValueError(f"No enabled secret versions found for secret '{secret_id}'")

        response = self.client.access_secret_version(name=latest_enabled_version.name)
        secret_value = response.payload.data.decode("UTF-8")
        return secret_id, secret_value

    def get_secrets(self, secret_ids: list[str]) -> dict[str, str]:
        """
        Accesses the payloads for the latest enabled versions of multiple secrets in parallel.

        Args:
            secret_ids (list[str]): A list of secret IDs to retrieve.

        Returns:
            dict[str, str]: A dictionary mapping secret IDs to their values.
        """
        secrets_values_dict = {}
        with ThreadPoolExecutor() as executor:
            future_to_secret = {executor.submit(self._get_single_secret, secret_id): secret_id for secret_id in secret_ids}
            for future in as_completed(future_to_secret):
                secret_id, secret_value = future.result()
                secrets_values_dict[secret_id] = secret_value

        return secrets_values_dict

    def upload_secret(self, file_path: str, secret_id: str) -> None:
        """
        Uploads a file content as a new secret version. Creates the secret if it doesn't exist.

        Args:
            file_path (str): The path to the file to upload.
            secret_id (str): The ID of the secret.
        """
        parent = f"projects/{self.project_id}"
        secret_path = self.client.secret_path(self.project_id, secret_id)

        try:
            self.client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": secret_id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
            print(f"Secret '{secret_id}' created.")
        except Exception as e:
            if "AlreadyExists" in str(e):
                print(f"Secret '{secret_id}' already exists, continuing to add version...")
            else:
                raise

        with open(file_path, "rb") as file:
            file_data = file.read()

        self.client.add_secret_version(
            request={
                "parent": secret_path,
                "payload": {"data": file_data},
            }
        )
        print(f"Secret '{secret_id}' updated with new version.")

    def get_credentials_from_secret(self, secret_id: str) -> service_account.Credentials:
        """
        Retrieves a secret, decodes it as JSON, and creates service account credentials.

        Args:
            secret_id (str): The ID of the secret containing the service account JSON.

        Returns:
            service_account.Credentials: The created credentials object.

        Raises:
            ValueError: If the secret content is not valid JSON.
        """
        try:
            secret_json = self.get_secrets([secret_id])[secret_id]
            service_account_info = json.loads(secret_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON from secret '{secret_id}': {e}")
        except KeyError:
            raise ValueError(f"Secret '{secret_id}' not found.")

        return service_account.Credentials.from_service_account_info(service_account_info)

    def download_secret_to_file(self, file_path: str, secret_id: str) -> None:
        """
        Downloads a secret and saves its content to a local file.

        Args:
            file_path (str): The local path to save the file.
            secret_id (str): The ID of the secret to download.
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        secret_content = self.get_secrets([secret_id])[secret_id]

        with open(file_path, "w") as f:
            f.write(secret_content)

        print(f"Secret '{secret_id}' downloaded and saved to '{file_path}'")


if __name__ == "__main__":
    # Example usage:
    try:
        # The project_id will be auto-detected from the environment
        secret_vault = SecretVault()

        # To get a secret
        # secrets = secret_vault.get_secrets(["your-secret-id"])
        # print(secrets)

        # To upload a secret
        # secret_vault.upload_secret("path/to/your/file.json", "your-secret-id")

        print("SecretVault initialized successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
