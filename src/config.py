import json
import os

from kivy.app import App
from kivy.utils import platform


class Config:
    def __init__(self):
        config_dir = os.path.join(os.path.dirname(__file__), "config")
        config_path = os.path.join(config_dir, "config.json")

        with open(config_path, "r") as file:
            self.config_data = json.load(file)

    @property
    def database_url(self):
        """データベースURLを取得

        Returns:
            str: database_url
        """
        if platform == "android":
            database_dir = App.get_running_app().user_data_dir
        else:
            database_dir = os.path.join(os.path.dirname(__file__), "database")

        return self.config_data.get("database_url", "").format(
            database_dir=database_dir
        )

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
