import time

import requests
from pypresence import Presence

from config import Config


class DiscordPresence:
    def __init__(self, client_id):
        self.rpc = Presence(client_id)
        self.rpc.connect()

    def update(self, details):
        self.rpc.update(details=details, start=time.time())

    def clear(self):
        self.rpc.clear()
        self.rpc.close()


class DiscordApi:
    def __init__(self):
        pass

    def get_app_name(self, client_id):
        config = Config()

        # リクエストを送信
        response = requests.get(config.get_discord_app_api_url(client_id))

        if response.status_code == 200:
            app_data = response.json()
            return app_data.get("name")
        else:
            return ""
