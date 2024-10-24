# src/drug_discovery/drug_formulation_optimization.py

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from skopt import gp_minimize
from skopt.space import Real, Categorical, Integer
from skopt.utils import use_named_args
from skopt.plots import plot_objective, plot_evaluations
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class DrugFormulationOptimizer:
    def __init__(self, formulation_space, efficacy_model, toxicity_model):
        self.formulation_space = formulation_space
        self.efficacy_model = efficacy_model
        self.toxicity_model = toxicity_model

    @staticmethod
    def create_formulation_space():
        """Create a formulation space with different variables."""
        formulation_space = [
            Real(0.1, 10.0, name='concentration'),
            Categorical(['A', 'B', 'C'], name='excipient'),
            Integer(1, 10, name='particle_size')
        ]
        return formulation_space

    @staticmethod
    def train_efficacy_model(data):
        """Train a random forest regressor to predict efficacy."""
        X = data[['concentration', 'excipient', 'particle_size']]
        y = data['efficacy']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        efficacy_model = RandomForestRegressor(n_estimators=100, random_state=42)
        efficacy_model.fit(X_train, y_train)
        return efficacy_model

    @staticmethod
    def train_toxicity_model(data):
        """Train a random forest regressor to predict toxicity."""
        X = data[['concentration', 'excipient', 'particle_size']]
        y = data['toxicity']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        toxicity_model = RandomForestRegressor(n_estimators=100, random_state=42)
        toxicity_model.fit(X_train, y_train)
        return toxicity_model

    @use_named_args(formulation_space)
    def objective_function(**params):
        """Evaluate the efficacy and toxicity of a formulation."""
        efficacy = DrugFormulationOptimizer.efficacy_model.predict(params)
        toxicity = DrugFormulationOptimizer.toxicity_model.predict(params)
        return -efficacy + toxicity  # Minimize toxicity and maximize efficacy

    def optimize_formulation(self):
        """Optimize the drug formulation using Bayesian optimization."""
        res_gp = gp_minimize(self.objective_function, self.formulation_space, n_calls=50, random_state=42)
        return res_gp

    def plot_results(self, res_gp):
        """Plot the optimization results."""
        plot_objective(res_gp)
        plot_evaluations(res_gp)
        plt.show()

    def save_results(self, res_gp, filename='optimization_results.npy'):
        """Save the optimization results to a file."""
        np.save(filename, res_gp)
        logging.info(f"Optimization results saved to {filename}.")

# Example usage
if __name__ == "__main__":
    # Create a sample dataset
    data = pd.DataFrame({
        'concentration': np.random.uniform(0.1, 10.0, 100),
        'excipient': np.random.choice(['A', 'B', 'C'], 100),
        'particle_size': np.random.randint(1, 10, 100),
        'efficacy': np.random.uniform(0.0, 1.0, 100),
        'toxicity': np.random.uniform(0.0, 1.0, 100)
    })

    # Train efficacy and toxicity models
    efficacy_model = DrugFormulationOptimizer.train_efficacy_model(data)
    toxicity_model = DrugFormulationOptimizer.train_toxicity_model(data)

    # Create a formulation space
    formulation_space = DrugFormulationOptimizer.create_formulation_space()

    # Initialize the optimizer
    optimizer = DrugFormulationOptimizer(formulation_space, efficacy_model, toxicity_model)

    # Optimize the formulation
    res_gp = optimizer.optimize_formulation()

    # Plot the results
    optimizer.plot_results(res_gp)

    # Save the results
    optimizer.save_results(res_gp)
