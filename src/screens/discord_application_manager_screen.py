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

# 手動でKVファイルをロード
Builder.load_file("kv/discord_application_manager_screen.kv")


class DiscordApplicationManagerScreen(Screen):
    applications = DictProperty({})
    new_client_id = StringProperty("")
    new_application_name = StringProperty("")

    def update_rv_data(self):
        self.ids.rv.data = [
            {
                "client_id": client_id,
                "name": name,
                "app_screen": self,
            }
            for client_id, name in self.applications.items()
        ]

    def on_pre_enter(self):
        with session_scope() as session:
            dao = DiscordApplicationDao(session)
            apps = dao.get_all_applications()
            self.applications = {app.client_id: app.name for app in apps}
        self.update_rv_data()

    def fetch_application_name(self):
        """Fetch the application name based on the new client ID."""
        if self.new_client_id.strip():
            discord_api = DiscordApi()
            self.new_application_name = discord_api.get_app_name(
                self.new_client_id.strip()
            )
        else:
            self.new_application_name = ""

    def add_application(self):
        client_id = self.new_client_id.strip()
        name = self.new_application_name.strip()
        if client_id and name:
            with session_scope() as session:
                dao = DiscordApplicationDao(session)
                new_app = dao.add_application(client_id, name)
                self.applications[new_app.client_id] = new_app.name
            self.update_rv_data()
            self.new_client_id = ""
            self.new_application_name = ""

    def go_back(self):
        self.manager.current = "main"


class DiscordApplicationItem(BoxLayout):
    client_id = StringProperty("")
    name = StringProperty("")
    app_screen = ObjectProperty(None)

    def toggle_edit(self):
        if self.is_editing:
            # Confirm edit
            self.confirm_edit(self.editing_client_id, self.editing_name)
        else:
            # Enter edit mode
            self.editing_client_id = self.client_id
            self.editing_name = self.name
            self.is_editing = True

    def confirm_edit(self, new_client_id, new_name):
        new_client_id = new_client_id.strip()
        new_name = new_name.strip()
        if new_client_id and new_name:
            with session_scope() as session:
                dao = DiscordApplicationDao(session)
                dao.update_application(self.client_id, new_client_id, new_name)
            # Update local data
            del self.app_screen.applications[self.client_id]
            self.client_id = new_client_id
            self.name = new_name
            self.app_screen.applications[self.client_id] = self.name
            self.app_screen.update_rv_data()
        self.is_editing = False

    def delete_application(self):
        with session_scope() as session:
            dao = DiscordApplicationDao(session)
            dao.logical_delete_by_client_id(self.client_id)
        del self.app_screen.applications[self.client_id]
        self.app_screen.update_rv_data()

    def cancel_edit(self):
        self.is_editing = False
