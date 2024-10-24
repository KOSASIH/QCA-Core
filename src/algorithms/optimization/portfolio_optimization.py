# src/algorithms/optimization/portfolio_optimization.py

import numpy as np
import pandas as pd
import cvxpy as cp
import matplotlib.pyplot as plt

class PortfolioOptimizer:
    def __init__(self, returns, risk_free_rate=0.01):
        self.returns = returns
        self.risk_free_rate = risk_free_rate
        self.num_assets = returns.shape[1]

    def optimize(self):
        """Optimize the portfolio using mean-variance optimization."""
        weights = cp.Variable(self.num_assets)
        expected_return = self.returns.mean().values @ weights
        risk = cp.quad_form(weights, self.returns.cov().values)

        # Objective: Maximize Sharpe Ratio
        objective = cp.Maximize((expected_return - self.risk_free_rate) / cp.sqrt(risk))
        constraints = [cp.sum(weights) == 1, weights >= 0]
        problem = cp.Problem(objective, constraints)
        problem.solve()

        return weights.value

    def simulate_portfolios(self, num_portfolios=10000):
        """Simulate random portfolios and calculate returns and risks."""
        results = np.zeros((3, num_portfolios))
        for i in range(num_portfolios):
            weights = np.random.random(self.num_assets)
            weights /= np.sum(weights)
            portfolio_return = np.dot(weights, self.returns.mean())
            portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(self.returns.cov(), weights)))
            results[0, i]= portfolio_return
            results[1, i] = portfolio_risk
            results[2, i] = portfolio_return / portfolio_risk

        return results

    def plot_efficient_frontier(self, results):
        """Plot the efficient frontier."""
        plt.figure(figsize=(10, 6))
        plt.scatter(results[1, :], results[0, :], c=results[2, :])
        plt.colorbar(label='Sharpe Ratio')
        plt.xlabel('Risk (Standard Deviation)')
        plt.ylabel('Expected Return')
        plt.title('Efficient Frontier')
        plt.show()

# Example usage
if __name__ == "__main__":
    returns = pd.read_csv('stock_returns.csv', index_col='Date', parse_dates=['Date'])
    optimizer = PortfolioOptimizer(returns)
    weights = optimizer.optimize()
    print("Optimal weights:", weights)

    results = optimizer.simulate_portfolios()
    optimizer.plot_efficient_frontier(results)
