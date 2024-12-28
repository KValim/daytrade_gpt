"""
ChatGPTClient module for automated interaction with ChatGPT.
"""

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time


class ChatGPTClientError(Exception):
    """Raised when ChatGPTClient fails to perform an operation."""


class ChatGPTClient:
    def __init__(self, debugger_address="127.0.0.1:9222"):
        """
        Initializes the ChatGPTClient for automated interaction via Selenium.
        """
        self.debugger_address = debugger_address
        self.driver = None

    def start_session(self):
        """
        Starts a browser session connected to an existing Edge debugging instance.
        """
        options = webdriver.EdgeOptions()
        options.add_experimental_option("debuggerAddress", self.debugger_address)
        try:
            self.driver = webdriver.Edge(
                service=Service(EdgeChromiumDriverManager().install()),
                options=options
            )
            print("Connected to Edge with debugging enabled.")
        except Exception as e:
            raise ChatGPTClientError(f"Failed to start Selenium session: {e}")

    def send_prompt(self, prompt: str) -> str:
        """
        Sends a prompt to ChatGPT and captures the response.
        """
        try:
            # Ensure ChatGPT is open
            self.driver.get("https://chatgpt.com/?temporary-chat=true")
            
            time.sleep(3)

            # Locate the input field and send the prompt
            textarea = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "prompt-textarea"))
            )
            textarea.clear()
            textarea.send_keys(prompt)

            # Locate and click the send button
            send_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='send-button']"))
            )
            send_button.click()

            # Wait for the response
            response_xpath = "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[1]/div/div/div/p"
            response_element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, response_xpath))
            )

            # Wait for the response to complete
            previous_text = ""
            while True:
                current_text = response_element.text
                if current_text == previous_text:
                    break
                previous_text = current_text
                time.sleep(2)

            return response_element.text
        except Exception as e:
            raise ChatGPTClientError(f"Failed to send prompt or capture response: {e}")

    def stop_session(self):
        """
        Stops the browser session.
        """
        if self.driver:
            self.driver.quit()
