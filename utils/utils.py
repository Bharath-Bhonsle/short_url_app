import hashlib
from datetime import datetime, timedelta, timezone


def generate_short_url(original_url: str) -> str:
    """Generate a consistent hash for the URL."""
    return hashlib.md5(str(original_url).encode()).hexdigest()[:6]


def get_expiration_time(hours: int) -> datetime:
    """Calculate the expiration datetime."""
    return datetime.now(timezone.utc) + timedelta(hours=hours)
