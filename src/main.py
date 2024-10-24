# src/main.py

import sqlite3  # Example for database connection
import multiprocessing as mp
from utils.data_loader import DataLoader
from utils.data_processor import DataProcessor
from utils.visualization import DataVisualizer

def load_data(loader):
    """Load data using the provided DataLoader instance."""
    data = loader.load_csv()
    if data is None:
        print("Failed to load data.")
    return data

def main():
    # Initialize DataLoader with a CSV file path or database connection
    csv_file_path = 'data/quantum_data.csv'  # Example CSV file path
    loader = DataLoader(file_path=csv_file_path)

    # Load data in parallel
    with mp.Pool(processes=2) as pool:
        data = pool.apply(load_data, (loader,))

    if data is None:
        return

    # Initialize DataProcessor with the loaded data
    processor = DataProcessor(data)

    # Normalize the data
    normalized_data = processor.normalize()

    # Filter the data based on a condition (example: value > 0.5)
    filtered_data = processor.filter_data('value > 0.5')

    # Extract specific features (example: ['feature1', 'feature2'])
    features = processor.extract_features(['feature1', 'feature2'])

    # Initialize DataVisualizer
    visualizer = DataVisualizer()

    # Visualize the normalized data
    visualizer.plot_histogram(normalized_data['value'], title='Normalized Data Histogram')

    # Visualize the filtered data
    visualizer.plot_scatter(filtered_data['feature1'], filtered_data['feature2'], title='Filtered Data Scatter Plot')

    # Visualize the correlation heatmap of the features
    correlation_matrix = features.corr()
    visualizer.plot_heatmap(correlation_matrix, title='Feature Correlation Heatmap')

    # Advanced Visualization: Pairplot for feature relationships
    visualizer.plot_pairplot(features, title='Feature Pairplot')

    # Advanced Visualization: Boxplot for outlier detection
    visualizer.plot_boxplot(normalized_data, title='Boxplot of Normalized Data')

if __name__ == "__main__":
    main()
