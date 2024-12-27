"""
ChatGPTClient module for manual interaction with ChatGPT.
"""

import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class ChatGPTClientError(Exception):
    """Raised when ChatGPTClient fails to perform an operation."""


class ChatGPTClient:
    """
    Prints the prompt for manual interaction with ChatGPT.
    """

    def __init__(self, cookies_file: str = "cookies.json"):
        """
        Initializes the ChatGPTClient (though we'll skip automated login).
        """
        self.cookies_file = cookies_file
        self.driver = None

    def start_session(self) -> None:
        """
        Starts a browser session - in this simplified version,
        we won't do anything besides initializing the driver if needed.
        """
        try:
            # Se ainda quiser abrir o Edge (não é realmente necessário, pois faremos tudo manualmente)
            service = Service(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service)
            self.driver.get("https://chat.openai.com/")
            print("Selenium session started, but no automated login is performed.")
            time.sleep(3)
        except Exception as err:
            raise ChatGPTClientError("Failed to start Selenium session.") from err

    def send_prompt(self, prompt: str) -> str:
        """
        Instead of sending prompt via Selenium, prints the prompt for manual use,
        then waits for user to paste the ChatGPT response back.
        """
        try:
            print("===== COPY THE PROMPT BELOW AND SEND IT MANUALLY IN YOUR BROWSER =====")
            print(prompt)
            print("===== AFTER GETTING THE RESPONSE FROM CHATGPT, PASTE IT BELOW =====")
            response = input("Paste the ChatGPT response here:\n> ")
            return response
        except Exception as err:
            raise ChatGPTClientError("Failed to process manual prompt/response.") from err

    def stop_session(self) -> None:
        """
        Closes the browser session if opened.
        """
        if self.driver:
            self.driver.quit()
