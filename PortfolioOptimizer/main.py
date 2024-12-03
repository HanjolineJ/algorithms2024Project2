from src.stock_fetcher import StockFetcher
from src.monte_carlo import MonteCarloSimulator
from src.risk_metrics import RiskMetrics
from src.heap_map import HeapMap


if __name__ == "__main__":
    fetcher = StockFetcher()
    tickers = ["AAPL", "BSX", "CAT", "DVA", "EMN", "FDX", "GRMN",
               "HLT", "IBM", "JBL", "LLY", "MAR" ]

    initial_investment = 10000

    portfolio_prices = fetcher.fetch_portfolio_prices(tickers)
    if portfolio_prices:
        simulator = MonteCarloSimulator(portfolio_prices, initial_investment)
        time_horizon = 365
        portfolio_values = simulator.simulate(num_simulations=500, time_horizon=time_horizon)

        if portfolio_values is not None:
            simulator.export_simulation_graph(portfolio_values)

            # Fetch S&P 500 daily returns for comparison
            sp500_returns = fetcher.fetch_snp500_daily_returns(time_horizon)  # This method should return daily S&P 500 returns as a numpy array
            
            # Export comparison graph (Monte Carlo vs S&P 500)
            if sp500_returns is not None:
                print (f"SP500 : {sp500_returns}")
                simulator.export_simulation_with_sp500_graph(portfolio_values, sp500_returns)


            risk_metrics = RiskMetrics(portfolio_values)
            risk_metrics.calculate_var()
            risk_metrics.plot_distribution()

            heap_map = HeapMap(portfolio_values, tickers)
            heap = heap_map.generate_heap()
            heap_map.display_heap(heap)
            heap_map.export_treemap(heap)
