"""
Extracts features from CSV data based on a provided configuration.
"""

import argparse
import pandas as pd

from config import Config
from extractor import FeatureExtractor
from utils.customlogger import CustomLogger

DEFAULT_CONFIG_PATH = "config.yaml"


def get_logger():
    """
    Initializes and returns a custom logger.
    Returns:
        logging.Logger: A logger instance specific to the feature extraction process.
    """
    return CustomLogger(name="Extract Feature").get_logger()


logger = get_logger()


def load_and_validate_config(config_path: str) -> Config:
    """
    Load and validate the configuration file.

    Args:
        config_path (str): The filesystem path to the configuration file.

    Returns:
        Config: A validated Config object.
    """
    config = Config(config_path)  # Initialize Config object with the provided path.
    if not config.validate():  # Validate the configuration.
        raise ValueError("Invalid configuration")  # Raise an exception if invalid.
    return config  # Return the validated configuration.


def extract_feature(extractor: FeatureExtractor) -> pd.DataFrame:
    """
    Process and filter CSV data using the provided Config.

    Args:
       extractor (FeatureExtractor): An instance of FeatureExtractor
            initialized with a validated configuration.

    Returns:
        pd.DataFrame: DataFrame containing the extracted features.
    """
    df = extractor.load_csv_with_types()  # Load CSV data with types.
    df_feature = extractor.extract_features(df)  # Extract features from the data.
    extractor.save_features(df_feature)  # Save the extracted features.
    return df_feature  # Return the DataFrame with features.


def create_extractor(config_path: str) -> FeatureExtractor:
    """
    Create a FeatureExtractor instance using the provided configuration.

    Args:
        config_path (str): Filesystem path to the configuration file.

    Returns:
        FeatureExtractor: An instance of FeatureExtractor.
    """
    config = load_and_validate_config(config_path)  # Load and validate the config.
    extractor = FeatureExtractor(config)  # Create FeatureExtractor using the config.
    return extractor  # Return the extractor.


def main(config_path: str = DEFAULT_CONFIG_PATH) -> None:
    """
    Main function to orchestrate the processing of CSV data.

    Args:
        config_path (str): Filesystem path to the configuration file.
            Defaults to 'config.yaml'.
    """
    extractor = create_extractor(config_path)  # Create FeatureExtractor.
    result_df = extract_feature(extractor)  # Extract features and obtain the DataFrame.
    logger.info("\n%s", str(result_df))  # Log the extracted features DataFrame.
    logger.info("Data processing complete.")  # Log the process completion.


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process CSV data based on a given configuration."
    )
    parser.add_argument(
        "--config_path",
        type=str,
        nargs="?",
        default=DEFAULT_CONFIG_PATH,
        help="Path to the configuration file",
    )
    args = parser.parse_args()  # Parse command-line arguments.
    main(args.config_path)  # Run the main function with provided config path.
