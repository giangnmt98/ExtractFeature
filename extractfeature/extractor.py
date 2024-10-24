"""
A module for extracting features from CSV files.

This module contains the FeatureExtractor class, which facilitates
loading CSV data, converting data types, extracting specific features,
and saving the extracted features to a CSV file.
"""

import numpy as np
import pandas as pd

from extractfeature.config import Config
from extractfeature.utils.custom_logger import CustomLogger


class FeatureExtractor:
    """
    A class to handle feature extraction from CSV files.

    Attributes:
        config (dict): Configuration for the feature extraction process.
        csv_path (str): Path to the input CSV file.
        fields (list): List of fields to be loaded from the CSV file.
        features (list): List of features to extract from the CSV data.
        logger (logging.Logger): Logger instance for logging messages.
    """

    def __init__(self, config: Config):
        """
        Initialize the FeatureExtractor with configuration settings.

        Args:
            config (Config): Configuration object containing settings for
                feature extraction.
        """
        self.config = config.config
        self.csv_path = self.config["input_data_path"]
        self.fields = self.config["fields"]
        self.features = [list(feature.keys())[0] for feature in self.config["feature"]]
        self.logger = CustomLogger(
            name="Feature Extraction", debug=self.config.get("debug", False)
        ).get_logger()

    @staticmethod
    def convert_data_types(df: pd.DataFrame, field_types: dict) -> pd.DataFrame:
        """
        Convert the data types of specified fields in a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame whose fields need type conversion.
            field_types (dict): Dictionary specifying the field names and their
                desired data types.

        Returns:
            pd.DataFrame: DataFrame with converted data types.
        """
        for field, dtype in field_types.items():
            # Convert field to specified data type
            df[field] = df[field].astype(dtype)
        return df

    def load_csv(
        self, csv_path: str, field_names: list, field_types: dict
    ) -> pd.DataFrame:
        """
        Load a CSV file and filter specific fields with required data types.

        Args:
            csv_path (str): Path to the CSV file to be loaded.
            field_names (list): List of field names to be loaded.
            field_types (dict): Dictionary specifying the field names and their
                corresponding data types.

        Returns:
            pd.DataFrame: DataFrame with loaded and type-converted fields.

        Raises:
            ValueError: If there is an error reading the CSV file.
        """
        try:
            # Log the loading process
            self.logger.info(
                "Loading CSV file from %s with fields %s", csv_path, field_names
            )
            df = pd.read_csv(csv_path, usecols=field_names)
            self.logger.info("CSV file loaded successfully")
            return self.convert_data_types(df, field_types)
        except pd.errors.EmptyDataError as e:
            self.logger.error("Error reading CSV file: %s", e)
            raise ValueError(f"Error reading CSV file: {e}") from e

    def load_csv_with_types(self) -> pd.DataFrame:
        """
        Load the CSV file using configurations and convert field data types.

        Returns:
            pd.DataFrame: DataFrame with the loaded and type-converted fields.
        """
        # Retrieve field definitions from configuration
        field_definitions = self.config.get("fields", [])

        # Extract field names and types
        field_names = [list(field.keys())[0] for field in field_definitions]
        field_types = {
            list(field.keys())[0]: list(field.values())[0]
            for field in field_definitions
        }

        # Load CSV data
        return self.load_csv(self.csv_path, field_names, field_types)

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract specific features from the provided DataFrame.

        Features extracted include:
        - `HasPhone`: Check if 'phone' is not null.
        - `EmailDomain`: Extract the domain part of 'email'.
        - `FirstNameLength`: Compute the length of 'first_name'.
        - `LastNameLength`: Compute the length of 'last_name'.
        - `IsInNY`: Check if 'state' equals 'NY'.

        Args:
            df (pd.DataFrame): DataFrame with the raw data.

        Returns:
            pd.DataFrame: DataFrame with extracted features.
        """
        self.logger.info("Starting feature extraction")

        # Replace invalid data with NaN
        df.replace(["nan", "NULL"], np.nan, inplace=True)

        # Check and extract 'HasPhone' feature
        if "HasPhone" in self.features:
            self.logger.info("Extracting 'HasPhone' feature")
            df["HasPhone"] = df["phone"].notnull()

        # Check and extract 'EmailDomain' feature
        if "EmailDomain" in self.features:
            self.logger.info("Extracting 'EmailDomain' feature")
            df["EmailDomain"] = df["email"].str.split("@").str[-1]

        # Check and extract 'FirstNameLength' feature
        if "FirstNameLength" in self.features:
            self.logger.info("Extracting 'FirstNameLength' feature")
            df["FirstNameLength"] = df["first_name"].str.len()

        # Check and extract 'LastNameLength' feature
        if "LastNameLength" in self.features:
            self.logger.info("Extracting 'LastNameLength' feature")
            df["LastNameLength"] = df["last_name"].str.len()

        # Check and extract 'IsInNY' feature
        if "IsInNY" in self.features:
            self.logger.info("Extracting 'IsInNY' feature")
            df["IsInNY"] = df["state"].str.upper() == "NY"

        self.logger.info("Feature extraction completed")
        return df

    def save_features(self, df: pd.DataFrame) -> None:
        """
        Save the extracted features to a CSV file.

        Args:
            df (pd.DataFrame): DataFrame containing the extracted features.
        """
        # Define output path from config
        output_path = self.config.get("output_data_path", "output.csv")
        self.logger.info("Saving features to %s", output_path)

        # Save DataFrame to CSV
        df.to_csv(output_path, index=False)
        self.logger.info("Features saved successfully")
