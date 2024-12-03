import numpy as np
import os
import matplotlib.pyplot as plt
import yfinance as yf
import heapq


class StockFetcher:
    def fetch_stock_price(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")
            if history.empty:
                raise ValueError(f"No data returned for {ticker}")
            price = history["Close"].iloc[-1]
            print(f"Fetched price for {ticker}: {price:.2f}")
            return price
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")
            return None

    def fetch_portfolio_prices(self, tickers):
        portfolio = {}
        for ticker in tickers:
            price = self.fetch_stock_price(ticker)
            if price:
                portfolio[ticker] = price
        if not portfolio:
            print("Error: No valid stock prices could be fetched.")
        return portfolio
    
    def fetch_snp500_daily_returns(self, time_horizon):
        """
        Fetch the daily returns for the S&P 500 index (^GSPC) for the given time horizon.
        """
        import yfinance as yf
        import numpy as np

        try:
            sp500 = yf.Ticker("^GSPC")
            history = sp500.history(period="2y")  # Fetch at least 2 years of data to cover weekends/holidays
            if history.empty:
                raise ValueError("No historical data returned for S&P 500 (^GSPC).")
        
            # Calculate daily percentage returns
            daily_returns = history['Close'].pct_change().dropna().values
        
            # Ensure the length matches the time_horizon
            if len(daily_returns) < time_horizon:
                raise ValueError(f"Not enough S&P 500 data for the specified time horizon ({time_horizon} days).")
        
            # Return the last `time_horizon` daily returns
            return daily_returns[-time_horizon:]
        except Exception as e:
            print(f"Error fetching S&P 500 daily returns: {e}")
            print("Generating simulated S&P 500 daily returns.")
            # Generate fallback random returns
            return np.random.normal(0.0005, 0.01, time_horizon)

