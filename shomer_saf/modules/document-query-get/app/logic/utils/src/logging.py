import logging

# Try to setup Cloud Logging, fallback to standard logging if not available
try:
    from google.cloud import logging as cloud_logging
    logging_client = cloud_logging.Client()
    logging_client.setup_logging()
except ImportError:
    # If google-cloud-logging is not available, use standard logging
    logging.basicConfig(level=logging.INFO)
except Exception:
    # If setup fails, use standard logging
    logging.basicConfig(level=logging.INFO)
    
    

# Get logger
logger = logging.getLogger(__name__)


def log_to_cloud_logging(level: str, message: str, **kwargs):
    """Log to Cloud Logging (or standard logging if Cloud Logging unavailable)"""
    log_func = getattr(logger, level.lower(), logger.info)
    if kwargs:
        log_func(f"{message} | {kwargs}")
    else:
        log_func(message)