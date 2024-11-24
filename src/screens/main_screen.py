from datetime import datetime

from kivy.properties import (
    BooleanProperty,
    DictProperty,
    ListProperty,
    StringProperty,
)
from kivy.uix.screenmanager import Screen
from pypresence import Presence

from dao import DetailDao, DiscordApplicationDao, LogDao
from database import session_scope
from services import DiscordPresence
from widgets.confirm_popup import ConfirmPopup


class MainScreen(Screen):
    main_categories = DictProperty({})
    sub_categories = DictProperty({})
    main_category_names = ListProperty()
    sub_category_contents = ListProperty()
    selected_client_id = StringProperty("")
    selected_main_category_name = StringProperty("")
    selected_sub_category = StringProperty("")
    is_running = BooleanProperty(False)
    presence = None  # Presenceオブジェクトを保持
    current_log_id = None  # 現在のログを保持

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_applications()

    def load_applications(self):
        with session_scope() as session:
            discord_application_dao = DiscordApplicationDao(session)
            self.main_categories = {
                app.name: app.client_id
                for app in discord_application_dao.get_all_applications()
            }
            self.main_category_names = list(self.main_categories.keys())

    def on_pre_enter(self):
        # 必要に応じてアプリケーション一覧を再読み込み
        # self.load_applications()

        # 選択されているメインカテゴリ名があれば、サブカテゴリを更新
        if self.selected_main_category_name:
            self.update_sub_categories(self.selected_main_category_name)

    # def on_sub_categories(self, instance, value):
    #     self.sub_category_contents = list(value.values())

    def update_sub_categories(self, selected_application_name):
        with session_scope() as session:
            detail_dao = DetailDao(session)
            self.sub_categories = {
                detail.id: detail.content
                for detail in detail_dao.get_detail_by_client_id(
                    self.main_categories[selected_application_name]
                )
            }
            self.sub_category_contents = list(self.sub_categories.values())
            if not self.is_running:
                self.selected_sub_category = ""

    def on_confirm(self):
        # client_id = (
        #     self.main_categories[self.selected_client_id]
        #     if self.selected_client_id
        #     else None
        # )
        if self.selected_client_id and self.selected_sub_category:
            if not self.is_running:
                self.show_presence(
                    self.selected_client_id, self.selected_sub_category
                )
                with session_scope() as session:
                    log_dao = LogDao(session)
                    detail_id = [
                        id
                        for id, content in self.sub_categories.items()
                        if content == self.selected_sub_category
                    ][0]
                    self.current_log_id = log_dao.add_log(
                        detail_id=detail_id
                    ).id
                self.is_running = True
            else:
                self.hide_presence()
                if self.current_log_id:
                    with session_scope() as session:
                        log_dao = LogDao(session)
                        log_dao.update_end_time(
                            self.current_log_id, datetime.now()
                        )
                        self.current_log_id = None
                self.is_running = False

    def go_to_subcategory_manager(self):
        self.manager.current = "subcategory_manager"

    def show_presence(self, client_id, detail):
        if self.presence is None or self.presence.loop._closed:
            self.presence = Presence(client_id)
            self.presence.connect()
            self.presence.update(details=detail)

    def hide_presence(self):
        if self.presence:
            self.presence.clear()  # プリセンスをクリア
            self.presence.close()  # Discordから切断
            # if self.presence.loop._closed:
            #     self.presence = None  # Presenceオブジェクトをリセット

    def go_to_discord_manager(self):
        self.manager.current = (
            "discord_application_manager"  # Discordアプリ管理画面に遷移
        )
