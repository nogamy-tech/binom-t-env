# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from datetime import datetime, timezone


def calculate_duration(timestamp) -> int:
    """
    Calculate duration in milliseconds from a timestamp to now.
    
    Args:
        timestamp: The timestamp to calculate duration from (datetime or str)
        
    Returns:
        int: Duration in milliseconds
    """
    now_utc = datetime.now(timezone.utc)
    
    # Handle string timestamp
    if isinstance(timestamp, str):
        # Normalize 'Z' to +00:00 and parse
        timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    
    # Ensure timestamp is timezone-aware
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    else:
        timestamp = timestamp.astimezone(timezone.utc)
    
    # Calculate duration in milliseconds
    duration_ms = int((now_utc - timestamp).total_seconds() * 1000)
    return duration_ms

