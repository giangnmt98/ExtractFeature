"""
This module provides a Config class to manage loading and validating
configuration files in YAML format.
"""

import yaml

from extractfeature.utils.utils import validate_config


class Config:
    """
    A class used to load and validate configuration files.

    Attributes:
        config_path (str): The filesystem path to the configuration file.
        config (dict): The loaded configuration data.

    Methods:
        __init__(config_path: str): Initializes the Config object,
            attempts to load and validate the configuration file.
        load_config() -> dict: Loads the configuration file.
        validate() -> bool: Validates the loaded configuration data.
    """

    def __init__(self, config_path: str):
        """
        Initializes the Config object.

        The constructor attempts to load the configuration file from the
        provided path. If the configuration is invalid, an exception is raised.

        Args:
            config_path (str): The filesystem path to the configuration file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            yaml.YAMLError: If there is an error parsing the YAML file.
            Exception: If the configuration validation fails.
        """
        self.config_path = config_path
        self.config = self.load_config()  # Load the configuration file
        if not self.validate():  # Validate the loaded configuration
            raise ValueError("Invalid configuration file.")

    def load_config(self) -> dict:
        """
        Loads the configuration file.

        Opens the configuration file located at config_path and parses it
        as YAML.

        Returns:
            dict: The loaded configuration data.

        Raises:
            FileNotFoundError: If the file does not exist.
            yaml.YAMLError: If there is an error parsing the YAML file.
        """
        with open(self.config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)  # Load and parse the YAML file

    def validate(self) -> bool:
        """
        Validates the loaded configuration data.

        Uses an external utility function to validate the configuration.

        Returns:
            bool: True if the configuration is valid, False otherwise.
        """
        return validate_config(self.config)  # Validate the configuration data
