"""
This module implements feature extraction from CSV data based on a configuration file.
"""

import numpy as np
import pandas as pd

from extractfeature.config import Config


class FeatureExtractor:
    """
    A class used to extract features from CSV data based on a given configuration.
    """
    def __init__(self, config: Config):
        """
        Initialize the FeatureExtractor with the configuration instance.

        Args:
            config (Config): An instance of Config containing the configuration data.
        """
        self.config = config.config
        self.csv_path = self.config["input_data_path"]
        self.fields = self.config["fields"]
        self.features = [list(feature.keys())[0] for feature in self.config["feature"]]

    @staticmethod
    def convert_data_types(df: pd.DataFrame, field_types: dict) -> pd.DataFrame:
        """
        Converts the data types of DataFrame columns.

        Args:
            df (pd.DataFrame): The DataFrame whose column types need to be converted.
            field_types (dict): A dictionary mapping field names to data types.

        Returns:
            pd.DataFrame: The DataFrame with updated data types.
        """
        for field, dtype in field_types.items():
            # Convert the data type of the specified field
            df[field] = df[field].astype(dtype)
        return df

    def load_csv(
        self, csv_path: str, field_names: list, field_types: dict
    ) -> pd.DataFrame:
        """
        Loads data from a CSV file and converts column data types.

        Args:
            csv_path (str): The path to the CSV file.
            field_names (list): List of field names to be read from the CSV file.
            field_types (dict): Dictionary mapping field names to data types.

        Returns:
            pd.DataFrame: The loaded and type-converted data.

        Raises:
            ValueError: If an error occurs reading the CSV file.
        """
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_path, usecols=field_names)
            return self.convert_data_types(df, field_types)
        except pd.errors.EmptyDataError as e:
            raise ValueError(f"Error reading CSV file: {e}") from e

    def load_csv_with_types(self) -> pd.DataFrame:
        """
        Load CSV data using field definitions from the configuration.

        Returns:
            pd.DataFrame: The loaded and type-converted data.
        """
        # Get the field definitions from the configuration
        field_definitions = self.config.get("fields", [])

        # Extract field names from the field definitions
        field_names = [list(field.keys())[0] for field in field_definitions]

        # Create a dictionary mapping field names to their data types
        field_types = {
            list(field.keys())[0]: list(field.values())[0]
            for field in field_definitions
        }
        return self.load_csv(self.csv_path, field_names, field_types)

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features as defined in the configuration.

        Args:
            df (pd.DataFrame): The input DataFrame
             from which features are to be extracted.

        Returns:
            pd.DataFrame: The DataFrame containing the extracted features.
        """
        # Replace "nan" and "NULL" strings with NaN values
        df.replace(["nan", "NULL"], np.nan, inplace=True)

        # Extract specific features based on configuration
        if "HasPhone" in self.features:
            df["HasPhone"] = df["phone"].notnull()
        if "EmailDomain" in self.features:
            df["EmailDomain"] = df["email"].str.split("@").str[-1]
        if "FirstNameLength" in self.features:
            df["FirstNameLength"] = df["first_name"].str.len()
        if "LastNameLength" in self.features:
            df["LastNameLength"] = df["last_name"].str.len()
        if "IsInNY" in self.features:
            df["IsInNY"] = df["state"].str.upper() == "NY"
        return df

    def save_features(self, df: pd.DataFrame) -> None:
        """
        Save the DataFrame with extracted features to a CSV file.

        Args:
            df (pd.DataFrame): The DataFrame containing the extracted features.
        """
        df.to_csv(self.config["output_data_path"], index=False)
