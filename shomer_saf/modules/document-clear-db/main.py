import base64
import json

from app.src.main_process import clear_db_process
from app.config import create_config_file, load_config
from app.services import GCPServiceFactory
from app.services.logging import ExecutionLogger

main_logger = ExecutionLogger(customer_id="document-clear-db")

@main_logger.log_execution
def main(event, context):
    """
    Cloud Function triggered by Pub/Sub.
    Expects a JSON message with a field "items" that is a list of strings.

    Example message:
    {
        "items": ["DnaTransaction1, DnaTransaction2, DnaTransaction3"]
    }
    """
    main_logger.set_context(customer_id="document-clear-db")
    main_logger.logger.info("Start document-clear-db")
    gcp_service_factory = GCPServiceFactory()
    create_config_file(gcp_service_factory=gcp_service_factory)

    try:
        # Decode the Pub/Sub message
        message_data = base64.b64decode(event["data"]).decode("utf-8")
        payload = json.loads(message_data)
    except Exception as e:
        main_logger.logger.exception(f"Failed to decode or parse message: {e}")
        print(f"Failed to decode or parse message: {e}")
        return "Invalid message format"

    print(f"Triggered by event {context.event_id} at {context.timestamp}")
    print(f"Topic: {context.resource['name']}")
    print(f"Payload: {payload}")

    # Health check
    if payload.get("health_check"):
        print("Health check successful")
        return "Health check successful"
    # Validate and extract list
    items = payload.get("items")

    if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
        main_logger.logger.exception("'items' must be a list of strings")
        print("'items' must be a list of strings")
        return "Invalid input: 'items' must be a list of strings"

    #  Main logic
    clear_db_process(gcp_service_factory, items)
    print("Process completed")

    return "Processing complete"

