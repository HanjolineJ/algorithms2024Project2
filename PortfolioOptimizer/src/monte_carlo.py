import numpy as np
import os
import matplotlib.pyplot as plt


class MonteCarloSimulator:
    def __init__(self, portfolio, initial_investment):
        if not portfolio or initial_investment <= 0:
            raise ValueError("Invalid portfolio or initial investment.")
        self.portfolio = portfolio
        self.initial_investment = initial_investment

    def simulate(self, num_simulations=1000, time_horizon=365):
        weights = np.array([1 / len(self.portfolio)] * len(self.portfolio))
        asset_prices = np.array(list(self.portfolio.values()))
        num_assets = len(self.portfolio)

        # Generate daily returns with per-asset variability
        asset_volatility = np.random.uniform(0.01, 0.05, num_assets)  # Volatility per asset
        daily_returns = np.random.normal(
            loc=0.001,  # Mean return
            scale=asset_volatility[:, np.newaxis],  # np.newaxis# Broadcast volatility for time and simulations
            size=(time_horizon, num_assets, num_simulations)
    )

        portfolio_values = np.zeros((time_horizon, num_simulations, num_assets))

        for i in range(num_assets):
            cumulative_returns = np.cumprod(1 + daily_returns[:, i, :], axis=0) - 1
            portfolio_values[:, :, i] = asset_prices[i] * (1 + cumulative_returns)

        return portfolio_values


    def export_simulation_graph(self, portfolio_values, filename="monte_carlo_simulation.png"):
        os.makedirs("graphs", exist_ok=True)
        filepath = os.path.join("graphs", filename)

        total_portfolio_values = portfolio_values.sum(axis=2)  # Sum across assets
        avg_values = total_portfolio_values.mean(axis=1)  # Average across simulations
        min_values = total_portfolio_values.min(axis=1)  # Minimum across simulations
        max_values = total_portfolio_values.max(axis=1)  # Maximum across simulations

        plt.figure(figsize=(10, 6))
        plt.plot(avg_values, color='blue', label='Average Portfolio Value')
        plt.fill_between(
            range(len(avg_values)),
            min_values,
            max_values,
            color='blue',
            alpha=0.1,
            label='Range of Portfolio Values'
        )
        plt.title('Monte Carlo Simulation for Portfolio Returns')
        plt.xlabel('Days')
        plt.ylabel('Portfolio Value')
        plt.legend()
        plt.grid()
        plt.savefig(filepath)
        print(f"Simulation graph saved as {filepath}")
        plt.show()


    def export_simulation_with_sp500_graph(self, portfolio_values, sp500_values, filename="monte_carlo_vs_sp500.png"):
        # import os
        # import numpy as np
        # import matplotlib.pyplot as plt

        os.makedirs("graphs", exist_ok=True)
        filepath = os.path.join("graphs", filename)

        # Aggregate portfolio values across simulations to get total portfolio value per time step
        total_portfolio_values = np.sum(portfolio_values, axis=2)
        avg_values = np.mean(total_portfolio_values, axis=1)
        min_values = np.min(total_portfolio_values, axis=1)
        max_values = np.max(total_portfolio_values, axis=1)

        sp500_cumulative = self.initial_investment * np.cumprod(1 + sp500_values)

        time_horizon = len(avg_values)
        if len(sp500_cumulative) != time_horizon:
            raise ValueError("Length of S&P 500 values does not match time horizon.")
        
        plt.figure(figsize=(12, 8))
        plt.plot(avg_values, color='blue', label='Portfolio Avg. Value', linewidth=1.5)

        plt.fill_between(
            range(time_horizon),
            min_values,
            max_values,
            color='blue',
            alpha=0.1,
            label='Portfolio Value Range'
        )

        plt.plot(sp500_cumulative, color='green', linestyle='--', label='S&P 500 Performance')

        plt.title('Monte Carlo Simulation vs S&P 500 Performance', fontsize=16, fontweight='bold')
        plt.xlabel('Days', fontsize=12)
        plt.ylabel('Portfolio Value', fontsize=12)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.legend(fontsize=12, loc='upper left', frameon=True)

        plt.savefig(filepath)
        print(f"Simulation graph with S&P 500 saved as {filepath}")
        plt.show()