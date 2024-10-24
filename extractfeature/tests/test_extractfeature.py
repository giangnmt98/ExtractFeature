"""
Unit tests for the FeatureExtractor class, testing various feature extraction methods.
"""

import unittest

import numpy as np
import pandas as pd

from extractfeature.config import Config
from extractfeature.extractor import FeatureExtractor


class TestFeatureExtractor(unittest.TestCase):
    """
    Unit tests for the FeatureExtractor class,
     testing various feature extraction methods.
    """

    def setUp(self):
        """
        Set up the test case environment, initializing
         the Config and FeatureExtractor instances,
        and set up a sample DataFrame for testing.
        """
        self.package_config = Config("extractfeature/tests/config/sample_config.yaml")
        self.extractor = FeatureExtractor(self.package_config)
        self.df = pd.DataFrame(
            {
                "phone": [np.nan, "1234567890", "0987654321", "1122334455"],
                "email": [
                    np.nan,
                    "jane@example.com",
                    "john@example.com",
                    "doe@example.com",
                ],
                "first_name": ["Jane", "John", "Doe", "Foo"],
                "last_name": ["Doe", "Doe", "Jane", "Bar"],
                "state": ["CA", "NY", "NJ", "CA"],
            }
        )

    def test_extract_has_phone_feature(self):
        """
        Test the extraction of the 'HasPhone' feature.

        Verifies that the method correctly identifies
         rows with or without phone numbers.
        """
        self.extractor.features = ["HasPhone"]

        # Extract features from the DataFrame
        result = self.extractor.extract_features(self.df)

        expected = [False, True, True, True]
        # Assert that the 'HasPhone' feature matches the expected list
        self.assertListEqual(result["HasPhone"].tolist(), expected)

    def test_extract_email_domain_feature(self):
        """
        Test the extraction of the 'EmailDomain' feature.

        Verifies that the method correctly extracts
         domain names from email addresses.
        """
        self.extractor.features = ["EmailDomain"]

        # Extract features from the DataFrame
        result = self.extractor.extract_features(self.df)

        expected = [np.nan, "example.com", "example.com", "example.com"]
        # Assert that the 'EmailDomain' feature matches the expected list
        self.assertListEqual(result["EmailDomain"].tolist(), expected)

    def test_extract_first_name_length_feature(self):
        """
        Test the extraction of the 'FirstNameLength' feature.

        Verifies that the method correctly computes the length of first names.
        """
        self.extractor.features = ["FirstNameLength"]

        # Extract features from the DataFrame
        result = self.extractor.extract_features(self.df)

        expected = [4, 4, 3, 3]
        # Assert that the 'FirstNameLength' feature matches the expected list
        self.assertListEqual(result["FirstNameLength"].tolist(), expected)

    def test_extract_last_name_length_feature(self):
        """
        Test the extraction of the 'LastNameLength' feature.

        Verifies that the method correctly computes the length of last names.
        """
        self.extractor.features = ["LastNameLength"]

        # Extract features from the DataFrame
        result = self.extractor.extract_features(self.df)

        expected = [3, 3, 4, 3]
        # Assert that the 'LastNameLength' feature matches the expected list
        self.assertListEqual(result["LastNameLength"].tolist(), expected)

    def test_extract_is_in_ny_feature(self):
        """
        Test the extraction of the 'IsInNY' feature.

        Verifies that the method correctly identifies
         rows where the state is New York (NY).
        """
        self.extractor.features = ["IsInNY"]

        # Extract features from the DataFrame
        result = self.extractor.extract_features(self.df)

        expected = [False, True, False, False]
        # Assert that the 'IsInNY' feature matches the expected list
        self.assertListEqual(result["IsInNY"].tolist(), expected)


if __name__ == "__main__":
    unittest.main()
