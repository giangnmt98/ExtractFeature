"""
This module provides functionality to validate configuration dictionaries.
"""


def validate_config(config: dict) -> bool:
    """
    Validates a configuration dictionary to ensure it contains the
    required keys.

    Args:
        config (dict): The configuration dictionary to validate.

    Returns:
        bool: True if the configuration contains all required keys,
        False otherwise.
    """

    # Define the list of required keys for the configuration
    required_keys = ["fields"]

    # Check if all required keys are present in the config dictionary
    return all(key in config for key in required_keys)
