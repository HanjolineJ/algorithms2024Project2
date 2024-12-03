import numpy as np
import os
import matplotlib.pyplot as plt
import yfinance as yf
import heapq

class RiskMetrics:
    def __init__(self, portfolio_values):
        if portfolio_values is None or not portfolio_values.size:
            raise ValueError("Invalid portfolio values.")
        self.portfolio_values = portfolio_values

    def calculate_var(self, confidence_level=0.95):
        final_values = self.portfolio_values[-1, :].sum(axis=1)
        var = np.percentile(final_values, (1 - confidence_level) * 100)
        print(f"Value at Risk (VaR) at {confidence_level * 100}% confidence: {var:.3f}")
        return var
    
    def calculate_es(self, confidence_level=0.95):
        """
        Calculate Expected Shortfall (ES) at the given confidence level.
        """
        final_values = self.portfolio_values[-1, :].sum(axis=1)
        var_threshold = np.percentile(final_values, (1 - confidence_level) * 100)
        es = final_values[final_values <= var_threshold].mean()
        print(f"Expected Shortfall (ES) at {confidence_level * 100}% confidence: {es:.3f}")
        return es
    
    def test_var():
        simulated_data = np.random.normal(1000, 100, (250, 500, 10))  # Example mock data
        risk_metrics = RiskMetrics(simulated_data)
        assert risk_metrics.calculate_var(0.95) > 0  # VaR should be positive for valid data

    

    def plot_distribution(self, filename="final_portfolio_distribution.png"):
        final_values = self.portfolio_values[-1, :].sum(axis=1)
        os.makedirs("graphs", exist_ok=True)

        plt.figure(figsize=(10, 6))
        plt.hist(final_values, bins=50, color='blue', edgecolor='black', alpha=0.7)
        plt.title('Distribution of Final Portfolio Values')
        plt.xlabel('Portfolio Value')
        plt.ylabel('Frequency')
        plt.grid()
        filepath = os.path.join("graphs", filename)
        plt.savefig(filepath)
        print(f"Portfolio distribution graph saved to: {filepath}")
        plt.show()

