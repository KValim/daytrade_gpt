"""
SheetsClient module for Google Sheets interaction, now handling timestamp columns.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SheetsClientError(Exception):
    """Raised when SheetsClient fails to perform an operation."""


class SheetsClient:
    """
    Updates trading records on Google Sheets.
    """

    SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    SHEET_NAME = "Trading Journal"

    def __init__(self, credentials_file: str = "credentials.json"):
        self.credentials_file = credentials_file
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, self.SCOPE)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open(self.SHEET_NAME).sheet1
        except Exception as err:
            raise SheetsClientError("Failed to initialize SheetsClient.") from err

    def append_trade(self, row_data: list) -> None:
        """
        Appends a new row of trade data to the Google Sheet.
        row_data should match the columns: [timestamp, ticker, last_action, close, sma_10, rsi_14, decision]
        """
        try:
            self.sheet.append_row(row_data)
        except Exception as err:
            raise SheetsClientError("Failed to append row to Google Sheet.") from err

    def get_last_action(self, ticker: str) -> str:
        """
        Returns the last action taken for a given ticker,
        by reading the Google Sheets records.
        """
        try:
            # Obtem todas as linhas da planilha (matriz de dados)
            all_records = self.sheet.get_all_values()  # Retorna lista de listas

            # Vamos supor que cada linha tem a estrutura:
            # [timestamp, ticker, last_action, close, sma_10, rsi_14, gpt_decision]
            # E a primeira linha é o cabeçalho
            if len(all_records) <= 1:
                # Nenhum registro além do cabeçalho
                return "NONE"

            # Filtra por ticker
            filtered = [
                row for row in all_records[1:]  # ignora cabeçalho
                if row[1] == ticker
            ]

            if not filtered:
                return "NONE"  # Ticker sem histórico

            # Pega a última linha referente ao ticker
            last_row = filtered[-1]

            # A "decisão do GPT" está na coluna 7 (índice 6).
            # A "last_action" que passamos para o GPT pode estar na coluna 3 (índice 2).
            # A depender de como você organiza, pode variar.
            # Digamos que a ação "mais recente" de fato é a "GPT Decision" da última linha
            last_decision = last_row[6]  # GPT Decision

            if last_decision in ("BUY", "SELL", "HOLD", "NOT_BUY"):
                return last_decision
            else:
                return "NONE"
        except Exception as err:
            raise SheetsClientError(f"Failed to get last action for {ticker}.") from err
