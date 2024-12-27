"""
DataCollector module responsible for fetching market data.
"""

import yfinance as yf
import pandas as pd


class DataCollectorError(Exception):
    """Raised when data collection fails."""


class DataCollector:
    """
    Collects market data from yfinance or another source.
    """

    DEFAULT_PERIOD: str = "1d"
    DEFAULT_INTERVAL: str = "5m"

    def fetch_data(self, ticker: str) -> pd.DataFrame:
        """
        Fetches market data for the specified ticker.
        """
        try:
            df = yf.download(
                ticker,
                period=self.DEFAULT_PERIOD,
                interval=self.DEFAULT_INTERVAL
            )
            if df.empty:
                raise DataCollectorError(f"No data found for {ticker}.")
            return df
        except Exception as err:
            raise DataCollectorError(f"Failed to fetch data for {ticker}.") from err
