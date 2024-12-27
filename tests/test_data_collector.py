import pytest
import pandas as pd
from trading_bot.data_collector import DataCollector, DataCollectorError

def test_fetch_data_valid_ticker(monkeypatch):
    def mock_download(*args, **kwargs):
        return pd.DataFrame({"Close": [10, 11, 12]})
    monkeypatch.setattr("yfinance.download", mock_download)

    collector = DataCollector()
    df = collector.fetch_data("TEST")
    assert not df.empty

def test_fetch_data_empty_response(monkeypatch):
    def mock_download(*args, **kwargs):
        return pd.DataFrame()
    monkeypatch.setattr("yfinance.download", mock_download)

    collector = DataCollector()
    with pytest.raises(DataCollectorError):
        collector.fetch_data("FAKE")
