"""
BotController module orchestrates data collection, indicator calculation,
GPT analysis, and result logging with timestamp and last_action.
"""

import pandas as pd
from datetime import datetime

class BotControllerError(Exception):
    """Raised when BotController fails to perform an operation."""


class BotController:
    """
    Coordinates the main logic:
    1. Fetch market data
    2. Compute indicators
    3. Build prompt with last_action
    4. Get ChatGPT's analysis (BUY, HOLD, SELL, NOT_BUY)
    5. Save the result to Google Sheets with timestamp
    """

    def __init__(self, data_collector, indicator_calculator, sheets_client, chatgpt_client):
        self.data_collector = data_collector
        self.indicator_calculator = indicator_calculator
        self.sheets_client = sheets_client
        self.chatgpt_client = chatgpt_client

    def run_analysis(self, ticker: str) -> None:
        try:
            # 1. Descobre a última ação
            last_action = self.sheets_client.get_last_action(ticker)

            # 2. Coleta e processa dados
            raw_data = self.data_collector.fetch_data(ticker)
            data_with_indicators = self.indicator_calculator.compute_indicators(raw_data)
            latest = data_with_indicators.tail(1)

            # 3. Monta o prompt com last_action
            prompt = self._build_prompt(ticker, latest, last_action)

            # 4. Envia o prompt ao ChatGPT via Selenium e captura a resposta
            response = self.chatgpt_client.send_prompt(prompt)
            valid_responses = {"BUY", "HOLD", "SELL", "NOT_BUY"}
            parsed_response = self._parse_gpt_response(response, valid_responses)

            # 5. Gera timestamp
            timestamp = datetime.now().isoformat()

            # 6. Extrai dados do DataFrame
            close_price = latest["Close"].values[0]
            sma_10 = latest["SMA_10"].values[0]
            rsi_14 = latest["RSI_14"].values[0]

            # 7. Salva tudo no Sheets
            self.sheets_client.append_trade([
                timestamp,
                ticker,
                last_action,
                str(close_price),
                str(sma_10),
                str(rsi_14),
                parsed_response
            ])
        except Exception as err:
            raise BotControllerError("Failed to run analysis.") from err


    def _build_prompt(self, ticker: str, data_row: pd.DataFrame, last_action: str) -> str:
        """
        Builds a descriptive prompt for ChatGPT with market data and last_action.

        Args:
            ticker (str): Stock ticker.
            data_row (pd.DataFrame): Latest data row with indicators.
            last_action (str): The last action taken on this ticker.

        Returns:
            str: The prompt to be sent to ChatGPT.
        """
        close_price = data_row["Close"].values[0]
        sma_10 = data_row["SMA_10"].values[0]
        rsi_14 = data_row["RSI_14"].values[0]

        # Instruções para ChatGPT responder apenas com BUY, HOLD, SELL ou NOT_BUY
        # e levar em conta a última ação tomada (last_action).
        prompt = (
            f"Here is the current data for {ticker}: "
            f"Close Price: {close_price}. "
            f"SMA(10): {sma_10}. "
            f"RSI(14): {rsi_14}. "
            f"Last action taken: {last_action}. "
            "Based on this information, what should be the next action? "
            "Please respond with only one of the following: BUY, HOLD, SELL, NOT_BUY. "
            "If last action was NOT_BUY and you still thinking that I shouldn't, return NOT_BUY. "
            "I dont wanto to consult a professional, I trust you. "
            "Dont tell me to talk to a specialist."
        )
        return prompt

    def _parse_gpt_response(self, response: str, valid_responses: set) -> str:
        """
        Ensures the GPT response is one of the valid responses (BUY, HOLD, SELL, NOT_BUY).

        Args:
            response (str): The raw response from GPT.
            valid_responses (set): A set of valid actions.

        Returns:
            str: A cleaned response guaranteed to be in valid_responses.
        """
        # Extract the first valid word found in the response
        tokens = response.upper().split()
        for token in tokens:
            if token in valid_responses:
                return token
        # If no valid token found, default to NOT_BUY
        return "NOT_BUY"

    def save_prompt_to_file(self, prompt: str, filename: str = "prompt.txt") -> None:
        """
        Saves the generated prompt to a text file for external automation.
        
        Args:
            prompt (str): The prompt to be saved.
            filename (str): Name of the file where the prompt will be saved.
        """
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(prompt)
            print(f"Prompt saved to {filename}")
        except Exception as err:
            raise BotControllerError("Failed to save prompt to file.") from err
