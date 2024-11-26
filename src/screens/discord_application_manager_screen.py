from kivy.app import App
from kivy.lang import Builder
from kivy.properties import (
    BooleanProperty,
    DictProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from dao import DiscordApplicationDao
from database import session_scope
from services import DiscordApi

# KVファイルを手動でロード
Builder.load_file("kv/discord_application_manager_screen.kv")


class DiscordApplicationManagerScreen(Screen):
    """Discordアプリケーション管理画面"""

    applications = DictProperty({})
    new_client_id = StringProperty("")
    new_application_name = StringProperty("")

    def update_rv_data(self):
        """リストビューのデータを更新"""
        self.ids.rv.data = [
            {
                "client_id": client_id,
                "name": name,
                "app_screen": self,
            }
            for client_id, name in self.applications.items()
        ]

    def on_pre_enter(self):
        """画面遷移前にアプリケーションを読み込む"""
        with session_scope() as session:
            dao = DiscordApplicationDao(session)
            apps = dao.get_all_applications()
            self.applications = {app.client_id: app.name for app in apps}
        self.update_rv_data()

    def fetch_application_name(self):
        """新しいクライアントIDに基づいてアプリケーション名を取得"""
        if self.new_client_id.strip():
            discord_api = DiscordApi()
            self.new_application_name = discord_api.get_app_name(
                self.new_client_id.strip()
            )
        else:
            self.new_application_name = ""

    def add_application(self):
        """新しいアプリケーションを追加"""
        client_id = self.new_client_id.strip()
        name = self.new_application_name.strip()
        if client_id and name:
            with session_scope() as session:
                dao = DiscordApplicationDao(session)
                new_app = dao.add_application(client_id, name)
                self.applications[new_app.client_id] = new_app.name
            self.update_rv_data()
            # 入力フィールドをクリア
            self.new_client_id = ""
            self.new_application_name = ""

    def go_back(self):
        """メイン画面に遷移"""
        self.manager.current = "main"


class DiscordApplicationItem(BoxLayout):
    """Discordアプリケーションアイテム"""

    client_id = StringProperty("")
    name = StringProperty("")
    app_screen = ObjectProperty(None)

    def delete_application(self):
        """アプリケーションを削除"""
        with session_scope() as session:
            dao = DiscordApplicationDao(session)
            dao.logical_delete_by_client_id(self.client_id)
        del self.app_screen.applications[self.client_id]
        # リストビューのデータを更新
        self.app_screen.update_rv_data()
