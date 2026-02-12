import tomli_w
import tomli
from pathlib import Path
from app.logic.utils.services import SecretVault, GCPServiceFactory


def config_secrets(gcp_service_factory: GCPServiceFactory = None):
    """Fetches specified secret values from the GCP Secret Manager."""
    if gcp_service_factory is None:
        gcp_service_factory = GCPServiceFactory()
    secret_vault = SecretVault(gcp_service_factory=gcp_service_factory)

    list_of_secret_ids = [
        "NOGAMY_IMAGE_MODEL",
        "NOGAMY_TEXT_MODEL",
        "NOGAMY_DOCUMENTAI_PROCESSOR_ID",
        "NOGAMY_FIRESTORE",
        "ACCOUNTS_FIRESTORE",
        "NOGAMY_WORKFLOW",
        "NOGAMY_BUCKET",
        "FIRESTORE_TIME_CLEAR_CUTOFF",
        "BUCKETS_TIME_CLEAR_CUTOFF",
    ]
    secret_values_dict = secret_vault.get_secrets(secret_ids=list_of_secret_ids)
    return secret_values_dict


def create_config_vars(gcp_service_factory: GCPServiceFactory = None):
    """Creates a dictionary of configuration variables, including secrets."""
    if gcp_service_factory is None:
        gcp_service_factory = GCPServiceFactory()

    secret_values_dict = config_secrets(gcp_service_factory=gcp_service_factory)

    """ Project Variables"""
    config_vars = {
        "project": {
            "image_model_name": secret_values_dict["NOGAMY_IMAGE_MODEL"],
            "text_model_name": secret_values_dict["NOGAMY_TEXT_MODEL"],
            "processor_id": secret_values_dict["NOGAMY_DOCUMENTAI_PROCESSOR_ID"],
            "location": "eu",
            "region": "me-west1",
            # "region": "europe-central2",
            "db_name": secret_values_dict["NOGAMY_FIRESTORE"],
            "accounts_db": secret_values_dict["ACCOUNTS_FIRESTORE"],
            "collection_name": "data",
            "accounts_collection": "accounts",
            "workflow_name": secret_values_dict["NOGAMY_WORKFLOW"],
            # "workflow_name":"workflow-test",
            "bucket": secret_values_dict["NOGAMY_BUCKET"],
            "documents_bucket": "documents_bucket_folder",
            "pages_bucket": "pages_bucket_folder",
            "data_bucket": "data_bucket_folder",
            "time_to_clear_firestore": int(secret_values_dict["FIRESTORE_TIME_CLEAR_CUTOFF"]),
            "time_to_clear_buckets": int(secret_values_dict["BUCKETS_TIME_CLEAR_CUTOFF"]),
        },
        "paths": {
            # Path variables
            "project_dir": str(Path(__file__).parents[3]),
            "data_dir": str(Path(__file__).parents[3] / "data"),
            "prompt_path": str(Path(__file__).parent / "base_prompt.txt"),
        },
    }

    return config_vars


def create_config_file(gcp_service_factory: GCPServiceFactory = None):
    """Creates a config.toml file with the project's configuration variables."""
    if gcp_service_factory is None:
        gcp_service_factory = GCPServiceFactory()

    env_vars = create_config_vars(gcp_service_factory=gcp_service_factory)

    # Write to TOML
    env_dir = Path(__file__).parent / "config.toml"
    with open(env_dir, "wb") as f:
        f.write(tomli_w.dumps(env_vars).encode("utf-8"))


def load_config():
    """Loads and returns the configuration from the config.toml file."""
    with open(Path(__file__).parent / "config.toml", "rb") as f:
        config = tomli.load(f)
    return config
