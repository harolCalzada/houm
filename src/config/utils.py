import os

def get_secret(key: str, default: str = '') -> str:
    """
    Get secret value from environment variable.
    """
    return os.getenv(key, default)
