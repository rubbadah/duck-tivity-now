import os

from kivy.app import App
from kivy.core.text import DEFAULT_FONT, LabelBase
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from sqlalchemy.orm import Session

from dao.detail_dao import DetailDao
from dao.log_dao import LogDao
from database import session_scope
from screens.discord_application_manager_screen import (
    DiscordApplicationManagerScreen,
)
from screens.main_screen import MainScreen
from screens.subcategory_manager_screen import SubcategoryManagerScreen
from utils.color_utils import rgb

# kvファイルのロード
Builder.load_file("kv/main_screen.kv")
Builder.load_file("kv/subcategory_manager_screen.kv")
Builder.load_file("kv/confirm_popup.kv")

# フォントファイルを指定
font_path = (
    "../src/font/NotoSansJP-Regular.ttf"  # フォントファイルへのパスを指定
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
        sm = MyScreenManager()

        # RGBの変換関数
        self.rgb = rgb
        return sm


if __name__ == "__main__":
    MyApp().run()
