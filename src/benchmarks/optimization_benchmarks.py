# src/benchmarks/optimization_benchmarks.py

import time
import numpy as np
import matplotlib.pyplot as plt
import logging
from scipy.optimize import minimize
from deap import base, creator, tools, algorithms

# Configure logging
logging.basicConfig(level=logging.INFO)

class OptimizationBenchmarks:
    def __init__(self, num_assets):
        self.num_assets = num_assets
        self.returns = np.random.rand(num_assets)  # Random returns for benchmarking

    def objective_function(self, weights):
        """Objective function for mean-variance optimization."""
        return -np.mean(self.returns @ weights) / np.sqrt(np.var(self.returns @ weights))

    def benchmark_gradient_descent(self):
        """Benchmark Gradient Descent optimization."""
        weights_init = np.random.rand(self.num_assets)
        weights_init /= np.sum(weights_init)  # Normalize weights

        start_time = time.time()
        result = minimize(self.objective_function, weights_init, method='BFGS', options={'disp': False})
        end_time = time.time()

        return end_time - start_time, result.fun

    def benchmark_genetic_algorithm(self):
        """Benchmark Genetic Algorithm optimization."""
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("weights", np.random.rand, self.num_assets)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.weights)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        def evaluate(individual):
            individual = np.array(individual)
            individual /= np.sum(individual)  # Normalize weights
            return self.objective_function(individual),

        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxBlend, alpha=0.5)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)

        population = toolbox.population(n=100)
        start_time = time.time()
        algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, verbose=False)
        end_time = time.time()

        fits = [ind.fitness.values[0] for ind in population]
        best_fit = min(fits)
        return end_time - start_time, best_fit

    def benchmark_simulated_annealing(self):
        """Benchmark Simulated Annealing optimization."""
        weights_init = np.random.rand(self.num_assets)
        weights_init /= np.sum(weights_init)  # Normalize weights

        start_time = time.time()
        result = minimize(self.objective_function, weights_init, method='L-BFGS-B', options={'disp': False})
        end_time = time.time()

        return end_time - start_time, result.fun

    def run_benchmarks(self):
        """Run all benchmarks and log results."""
        results = {}
        results['Gradient Descent'] = self.benchmark_gradient_descent()
        results['Genetic Algorithm'] = self.benchmark_genetic_algorithm()
        results['Simulated Annealing'] = self.benchmark_simulated_annealing()

        for algorithm, (time_taken, objective_value) in results.items():
            logging.info(f"{algorithm} - Time: {time_taken:.6f} seconds, Objective Value: {objective_value:.6f}")

        return results

    def plot_results(self, results):
        """Plot the benchmark results."""
        algorithms = list(results.keys())
        times = [results[alg][0] for alg in algorithms]
        objective_values = [results[alg][1] for alg in algorithms]

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Algorithms')
        ax1.set_ylabel('Time (seconds)', color=color)
        ax1.bar(algorithms, times, color=color, alpha=0.6, label='Time')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Objective Value', color=color)
 ax2.plot(algorithms, objective_values, color=color, alpha=0.6, label='Objective Value')
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    num_assets = 10
    benchmark = OptimizationBenchmarks(num_assets)
    results = benchmark.run_benchmarks()
    benchmark.plot_results(results)
