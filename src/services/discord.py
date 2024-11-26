import time

import requests
from pypresence import Presence

from config import Config


class DiscordPresence:
    """Discordのプレゼンス関連"""

    def __init__(self, client_id):
        """クラスの初期化

        Args:
            client_id (str): DiscordアプリケーションのクライアントID
        """
        self.rpc = Presence(client_id)
        self.rpc.connect()

    def update(self, details):
        """プレゼンスの情報を更新するメソッド

        Args:
            details (str): 表示する内容
        """
        self.rpc.update(details=details, start=time.time())  # プレゼンスを更新

    def clear(self):
        """プレゼンス表示解除"""
        self.rpc.clear()  # プレゼンスをクリア
        self.rpc.close()  # Discordから切断


class DiscordApi:
    """Discord APIとの通信"""

    def __init__(self):
        pass

    def get_app_name(self, client_id):
        """Discordアプリケーションの名前を取得

        Args:
            client_id (str): DiscordアプリケーションのクライアントID

        Returns:
            str: アプリケーションの名前（取得できなかった場合は空文字）
        """
        config = Config()  # 設定を取得

        # リクエストを送信
        response = requests.get(config.get_discord_app_api_url(client_id))

        if response.status_code == 200:
            app_data = response.json()
            return app_data.get("name")
        else:
            return ""
