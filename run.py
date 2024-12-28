"""
Main script to run the trading bot analysis.
"""

from trading_bot.factory import get_bot_controller


def main():
    bot_controller = get_bot_controller()
    bot_controller.chatgpt_client.start_session()
    try:
        # Exemplo de ticker
        bot_controller.run_analysis("PETR4.SA")
        bot_controller.run_analysis("VALE3.SA")
    finally:
        bot_controller.chatgpt_client.stop_session()


if __name__ == "__main__":
    main()
