# utils/data_processor.py

import numpy as np
import pandas as pd
import logging

class DataProcessor:
    def __init__(self, data):
        self.data = data
        logging.basicConfig(level=logging.INFO)

    def normalize(self):
        """Normalize the data to a range of [0, 1]."""
        if self.data is None:
            raise ValueError("Data must be loaded before processing.")
        normalized_data = (self.data - self.data.min()) / (self.data.max() - self.data.min())
        logging.info("Data normalized")
        return normalized_data

    def filter_data(self, condition):
        """Filter the data based on a condition."""
        filtered_data = self.data.query(condition)
        logging.info("Data filtered")
        return filtered_data

    def extract_features(self, feature_columns):
        """Extract specific features from the data."""
        features = self.data[feature_columns]
        logging.info("Features extracted")
        return features
