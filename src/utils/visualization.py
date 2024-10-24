# utils/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import logging

class DataVisualizer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def plot_histogram(self, data, title='Histogram', xlabel='Value', ylabel='Frequency'):
        """Plot a histogram of the data."""
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=30, alpha=0.7, color='blue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid()
        plt.show()
        logging.info("Histogram plotted")

    def plot_scatter(self, x, y, title='Scatter Plot', xlabel='X-axis', ylabel='Y-axis'):
        """Plot a scatter plot of the data."""
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, alpha=0.7, color='red')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid()
        plt.show()
        logging.info("Scatter plot plotted")

    def plot_heatmap(self, data, title='Heatmap'):
        """Plot a heatmap of the data."""
        plt.figure(figsize=(10, 6))
        sns.heatmap(data, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title(title)
        plt.show()
        logging.info("Heatmap plotted")

    def plot_pairplot(self, data, title='Pairplot'):
        """Plot a pairplot of the features."""
        plt.figure(figsize=(12, 10))
        sns.pairplot(data)
        plt.suptitle(title, y=1.02)
        plt.show()
        logging.info("Pairplot plotted")

    def plot_boxplot(self, data,title='Boxplot'):
        """Plot a boxplot of the data."""
        plt.figure(figsize=(10, 6))
        plt.boxplot(data, vert=True, patch_artist=True)
        plt.title(title)
        plt.show()
        logging.info("Boxplot plotted")
