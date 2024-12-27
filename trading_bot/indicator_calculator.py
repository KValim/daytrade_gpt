"""
IndicatorCalculator module responsible for computing technical metrics.
"""

import pandas as pd
import ta


class IndicatorError(Exception):
    """Raised when indicator calculation fails."""


class IndicatorCalculator:
    """
    Calculates common technical indicators.
    """

    def compute_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Adds technical indicators to the DataFrame.
        """
        if data.empty:
            raise IndicatorError("DataFrame is empty. Cannot compute indicators.")

        data = data.copy()
        try:
            data['SMA_10'] = ta.trend.sma_indicator(data['Close'], window=10)
            data['RSI_14'] = ta.momentum.rsi(data['Close'], window=14)
            data['Volatility'] = data['Close'].pct_change().rolling(window=10).std() * 100
            data['Bollinger_High'] = ta.volatility.bollinger_hband(data['Close'], window=20)
            data['Bollinger_Low'] = ta.volatility.bollinger_lband(data['Close'], window=20)
        except KeyError as err:
            raise IndicatorError("Missing 'Close' column in data.") from err

        return data
