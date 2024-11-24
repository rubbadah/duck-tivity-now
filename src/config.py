import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE_PATH = "./config/config.json"


class Config:
    def __init__(self):
        # try:
        with open(CONFIG_FILE_PATH, "r") as file:
            self.config_data = json.load(file)

    @property
    def database_url(self):
        """
        Returns:
            string: database_url
        """
        return self.config_data.get("database_url", "")

    @property
    def discord_app_api_url(self):
        """
        Returns:
            string: discord_bot_token
        """
        return self.config_data.get("discord_app_api_url", "")

    def get_discord_app_api_url(self, client_id):
        # HACK: Discord APIのレートリミットの対策はした方がいいかも
        """
        Returns:
            string: discord_bot_token
        """
        return self.config_data.get("discord_app_api_url", "").format(
            client_id=client_id
        )
