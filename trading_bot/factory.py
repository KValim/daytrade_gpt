"""
Factory module to create instances of trading bot components.
"""

from trading_bot.data_collector import DataCollector
from trading_bot.indicator_calculator import IndicatorCalculator
from trading_bot.sheets_client import SheetsClient
from trading_bot.chatgpt_client import ChatGPTClient
from trading_bot.bot_controller import BotController


def get_bot_controller() -> BotController:
    """
    Returns an instance of BotController with all dependencies.
    """
    data_collector = DataCollector()
    indicator_calculator = IndicatorCalculator()
    sheets_client = SheetsClient()
    chatgpt_client = ChatGPTClient()

    bot_controller = BotController(
        data_collector=data_collector,
        indicator_calculator=indicator_calculator,
        sheets_client=sheets_client,
        chatgpt_client=chatgpt_client
    )
    return bot_controller
