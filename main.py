import pickle
import threading

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from timeloop import Timeloop
from selenium import webdriver
from datetime import timedelta
# from trainer import bot


class AnnoyingBuzzrBot:
    def __init__(self):
        self._driver = webdriver.Chrome()
        self._long_wait = WebDriverWait(self._driver, 30)
        self._quick_wait = WebDriverWait(self._driver, 3)
        self._stranger_messages_idx = 1

    def run(self):
        self._driver.get("http://www.buzzr.com.br/chat.html")

        self._findElements()
        self._waitConversationToStart()
        self._monitorConversationEnding()
        self._sendHi()

        while True:
            try:
                paragraph = self._quick_wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='chatarea']/p[@class='theirmsg'][{}]".format(self._stranger_messages_idx))))
            except:
                continue

            if paragraph:
                self._stranger_messages_idx += 1

                text = paragraph.text
                text = text.split("Estranho:")[1]

                try:
                    print("User Message:", text)
                    # response = bot.get_response(text)

                    self.chat.clear()
                    self.chat.send_keys(text[::-1])
                    self.send.click()
                except:
                    continue

    def _waitConversationToStart(self):
        self._long_wait.until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "sysmsg"), "Você já está falando com alguém. Diga oi!"))

    def _findElements(self):
        self.send = self._driver.find_element_by_id("btnsend")
        self.chat = self._driver.find_element_by_id("chatinput")

    def _sendHi(self):
        self.chat.send_keys("Oi")
        self.send.click()

    def _monitorConversationEnding(self):
        self.tl = Timeloop()

        @self.tl.job(interval=timedelta(seconds=5))
        def check_end_of_chat():
            next_btn = self._driver.find_elements_by_id("btnnext")

            if len(next_btn) > 0:
                self._stranger_messages_idx = 1

                next_btn[0].click()

                self._quick_wait.until(
                    EC.element_to_be_clickable((By.ID, "btnsend")))

                self._sendHi()

        self.tl.start(block=False)


if __name__ == "__main__":
    bot = AnnoyingBuzzrBot()
    bot.run()
