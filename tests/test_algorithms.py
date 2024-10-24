# tests/test_algorithms.py

import unittest
import numpy as np

def example_algorithm(data):
    """A simple example algorithm that returns the mean of the data."""
    return np.mean(data)

class TestAlgorithms(unittest.TestCase):
    def test_example_algorithm(self):
        data = [1, 2, 3, 4, 5]
        result = example_algorithm(data)
        self.assertEqual(result, 3)

    def test_example_algorithm_empty(self):
        data = []
        with self.assertRaises(ValueError):
            example_algorithm(data)

if __name__ == '__main__':
    unittest.main()
