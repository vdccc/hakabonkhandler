import requests

from config import TgConfig

class Alert():

    def send(text):
        pass


class TgAlert(Alert):

    def __init__(self):
       self.url = TgConfig.api_url + TgConfig.bot_method

    def send(self, text):
        if TgConfig.bot_method is None:
            return

        data = {
            "chat_id": TgConfig.chat_id,
            "text": text
        }

        requests.post(self.url, data)
