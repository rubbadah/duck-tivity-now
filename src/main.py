import asyncio
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import DEFAULT_FONT, LabelBase
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform

from dao.detail_dao import DetailDao
from dao.log_dao import LogDao
from database import session_scope
from screens.discord_application_manager_screen import (
    DiscordApplicationManagerScreen,
)
from screens.main_screen import MainScreen
from screens.subcategory_manager_screen import SubcategoryManagerScreen
from utils.color_utils import rgb

# Androidの場合、パーミッションを要求
if platform == "android":
    from android.permissions import Permission, request_permissions

    request_permissions([Permission.INTERNET])

# kvファイルのロード
Builder.load_file("kv/main_screen.kv")
Builder.load_file("kv/subcategory_manager_screen.kv")
Builder.load_file("kv/confirm_popup.kv")

# フォントファイルを指定
font_path = os.path.join(
    os.path.dirname(__file__), "font", "NotoSansJP-Regular.ttf"
)
resource_add_path(os.path.dirname(font_path))
LabelBase.register(DEFAULT_FONT, font_path)


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(MainScreen(name="main"))
        self.add_widget(SubcategoryManagerScreen(name="subcategory_manager"))
        self.add_widget(
            DiscordApplicationManagerScreen(name="discord_application_manager")
        )


class MyApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    MyApp().run()
