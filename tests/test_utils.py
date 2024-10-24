# tests/test_utils.py

import unittest
import pandas as pd
from utils.data_loader import DataLoader
from utils.data_processor import DataProcessor

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader(file_path='data/test_data.csv')  # Use a test CSV file

    def test_load_csv(self):
        data = self.loader.load_csv()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, pd.DataFrame)

    def test_load_csv_invalid(self):
        self.loader.file_path = 'invalid_path.csv'
        with self.assertRaises(ValueError):
            self.loader.load_csv()

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'value': [0.1, 0.2, 0.3, 0.4, 0.5],
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1]
        })
        self.processor = DataProcessor(self.data)

    def test_normalize(self):
        normalized_data = self.processor.normalize()
        self.assertTrue((normalized_data['value'] >= 0).all())
        self.assertTrue((normalized_data['value'] <= 1).all())

    def test_filter_data(self):
        filtered_data = self.processor.filter_data('value > 0.3')
        self.assertEqual(len(filtered_data), 2)

    def test_extract_features(self):
        features = self.processor.extract_features(['feature1', 'feature2'])
        self.assertEqual(features.shape[1], 2)

if __name__ == '__main__':
    unittest.main()
