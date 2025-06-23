from os import getenv
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    load_dotenv()


def get_env_value(key: str, default: str = None) -> str:
    """
    Get environment variable value.

    Args:
        key: Environment variable name
        default: Default value if environment variable is not found

    Returns:
        str: Environment variable value or default value
    """
    return getenv(key, default)
