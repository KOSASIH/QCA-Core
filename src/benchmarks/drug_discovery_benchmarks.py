# src/benchmarks/drug_discovery_benchmarks.py

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.neural_network import MLPRegressor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class DrugDiscoveryBenchmarks:
    def __init__(self, data):
        self.data = data
        self.models = {
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Support Vector Machine': SVR(),
            'Neural Network': MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
        }

    def benchmark_model(self, model):
        """Benchmark the training and evaluation of the model."""
        X = self.data[['concentration', 'excipient', 'particle_size']]
        y = self.data['efficacy']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions.round())
        precision = precision_score(y_test, predictions.round(), average='weighted', zero_division=0)
        recall = recall_score(y_test, predictions.round(), average='weighted', zero_division=0)
        f1 = f1_score(y_test, predictions.round(), average='weighted', zero_division=0)

        return training_time, accuracy, precision, recall, f1

    def run_benchmarks(self):
        """Run benchmarks for all models and log results."""
        results = {}
        for model_name, model in self.models.items():
            training_time, accuracy, precision, recall, f1 = self.benchmark_model(model)
            results[model_name] = {
                'Training Time': training_time,
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1 Score': f1
            }
            logging.info(f"{model_name} - Training Time: {training_time:.6f} seconds, "
                         f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, "
                         f"Recall: {recall:.4f}, F1 Score: {f1:.4f}")

        return results

    def plot_results(self, results):
        """Plot the benchmark results."""
        metrics = ['Training Time', 'Accuracy', 'Precision', 'Recall', 'F1 Score']
        for metric in metrics:
            plt.figure(figsize=(10, 6))
            plt.bar(results.keys(), [results[model][metric] for model in results.keys()])
            plt.title(f'{metric} Comparison')
            plt.ylabel(metric)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

# Example usage
if __name__ == "__main__":
    # Create a sample dataset
    data = pd.DataFrame({
        'concentration': np.random.uniform(0.1, 10.0, 100),
        'excipient': np.random.choice(['A', 'B', 'C'], 100),
        'particle_size': np.random.randint(1, 10, 100),
        'efficacy': np.random.uniform(0.0, 1.0, 100)
    })

    benchmark = DrugDiscoveryBenchmarks(data)
    results = benchmark.run_benchmarks()
    benchmark.plot_results(results)
