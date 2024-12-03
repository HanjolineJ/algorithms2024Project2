# import requests
# import time


# class StockFetcher:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.base_url = "https://www.alphavantage.co/query"

#     def fetch_stock_price(self, ticker):
#         """Fetches the current price of a stock."""
#         try:
#             params = {
#                 "function": "GLOBAL_QUOTE",
#                 "symbol": ticker,
#                 "apikey": self.api_key
#             }
#             response = requests.get(self.base_url, params=params)
#             data = response.json()
#             print(f"Raw data for {ticker}: {data}")  # Debugging raw API response
#             if "Global Quote" in data and "05. price" in data["Global Quote"]:
#                 price = float(data["Global Quote"]["05. price"])
#                 print(f"Fetched price for {ticker}: {price}")
#                 return price
#             else:
#                 print(f"Error: Unexpected response format for {ticker}")
#                 return None
#         except Exception as e:
#             print(f"Error fetching price for {ticker}: {e}")
#             return None

#     def fetch_portfolio_prices(self, tickers):
#         """Fetches prices for a list of tickers, respecting API rate limits."""
#         portfolio = {}
#         for ticker in tickers:
#             price = self.fetch_stock_price(ticker)
#             if price:
#                 portfolio[ticker] = price
#             time.sleep(1)  # Respect API rate limits (5 requests/minute)
#         return portfolio


# import yfinance as yf


# class StockFetcher:
#     def __init__(self):
#         pass

#     def fetch_stock_price(self, ticker):
#         """Fetches the current price of a stock using Yahoo Finance."""
#         try:
#             stock = yf.Ticker(ticker)
#             price = stock.history(period="1d")["Close"].iloc[-1]  # Get the latest closing price
#             print(f"Fetched price for {ticker}: {price:.2f}")
#             return price
#         except Exception as e:
#             print(f"Error fetching price for {ticker}: {e}")
#             return None

#     def fetch_portfolio_prices(self, tickers):
#         """Fetches prices for a list of tickers."""
#         portfolio = {}
#         for ticker in tickers:
#             price = self.fetch_stock_price(ticker)
#             if price:
#                 portfolio[ticker] = price
#         return portfolio

# import yfinance as yf

# class StockFetcher:
#     def __init__(self):
#         pass

#     def fetch_stock_price(self, ticker):
#         """
#         Fetches the current price of a stock using Yahoo Finance.
#         """
#         try:
#             stock = yf.Ticker(ticker)
#             price = stock.history(period="1d")["Close"].iloc[-1]  # Get the latest closing price
#             print(f"Fetched price for {ticker}: {price:.2f}")
#             return price
#         except Exception as e:
#             print(f"Error fetching price for {ticker}: {e}")
#             return None

#     def fetch_portfolio_prices(self, tickers):
#         """
#         Fetches prices for a list of tickers.
#         """
#         portfolio = {}
#         for ticker in tickers:
#             price = self.fetch_stock_price(ticker)
#             if price:
#                 portfolio[ticker] = price
#         return portfolio

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
    

    # def fetch_snp500_daily_returns(self):
    #     """
    #     Fetch the daily returns for the S&P 500 index (^GSPC) for the past year.
    #     """
    #     try:
    #         sp500 = yf.Ticker("^GSPC")
    #         history = sp500.history(period="1y")  # Fetch 1-year historical data
    #         if history.empty:
    #             raise ValueError("No historical data returned for S&P 500 (^GSPC).")
    #         daily_returns = history['Close'].pct_change().dropna().values  # Calculate daily returns
    #         print(f"Fetched S&P 500 daily returns for the past year.")
    #         return daily_returns
    #     except Exception as e:
    #         print(f"Error fetching S&P 500 daily returns: {e}")
    #         return None


    def fetch_snp500_daily_returns(self, time_horizon):
        """
        Fetch the daily returns for the S&P 500 index (^GSPC) for the given time horizon.
        """
        import yfinance as yf

        try:
            sp500 = yf.Ticker("^GSPC")
            # Fetch historical data for at least the time_horizon number of days
            history = sp500.history(period=f"{time_horizon + 10}d")  # Fetch a bit more to account for weekends/holidays
            if history.empty:
                raise ValueError("No historical data returned for S&P 500 (^GSPC).")
            
            # Calculate daily returns
            daily_returns = history['Close'].pct_change().dropna().values

            # Ensure the length matches the time_horizon
            if len(daily_returns) < time_horizon:
                raise ValueError("Insufficient data for S&P 500 to match the time horizon.")
            return daily_returns[:time_horizon]
        except Exception as e:
            print(f"Error fetching S&P 500 daily returns: {e}")
            return None
    
