import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE_PATH = "./config/config.json"


class Config:
    def __init__(self):
        # try:
        with open(CONFIG_FILE_PATH, "r") as file:
            self.config_data = json.load(file)
        # HACK: そのままエラーを返すならここでキャッチしなくていいのでは？
        # except FileNotFoundError:
        #     raise Exception(f"Not found: {CONFIG_FILE_PATH}")
        # except json.JSONDecodeError:
        #     raise Exception(f"JSON decode error: {CONFIG_FILE_PATH}")

    @property
    def database_url(self):
        """
        Returns:
            string: database_url
        """
        return self.config_data.get("database_url", "")

    @property
    def discord_app_api_url(self, client_id):
        """
        Returns:
            string: discord_bot_token
        """
        return self.config_data.get("discord_app_api_url", "").format(
            client_id=client_id
        )


# 使用例
#     config = Config('config.json')

# config.data_file, config.initial_balance などでアクセス
