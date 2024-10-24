# utils/data_loader.py

import pandas as pd
import numpy as np
import logging

class DataLoader:
    def __init__(self, file_path=None):
        self.file_path = file_path
        logging.basicConfig(level=logging.INFO)

    def load_csv(self):
        """Load data from a CSV file."""
        if not self.file_path:
            raise ValueError("File path must be provided.")
        try:
            data = pd.read_csv(self.file_path)
            logging.info(f"Loaded data from {self.file_path}")
            return data
        except Exception as e:
            logging.error(f"Error loading CSV: {e}")
            return None

    def load_from_database(self, query, connection):
        """Load data from a database using a SQL query."""
        try:
            data = pd.read_sql(query, connection)
            logging.info("Loaded data from database")
            return data
        except Exception as e:
            logging.error(f"Error loading from database: {e}")
            return None
