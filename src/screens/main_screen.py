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
    presence = None
    current_log_id = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_applications()

    def load_applications(self):
        """アプリケーションの一覧をデータベースから読み込む"""
        with session_scope() as session:
            discord_application_dao = DiscordApplicationDao(session)
            self.main_categories = {
                app.name: app.client_id
                for app in discord_application_dao.get_all_applications()
            }
            self.main_category_names = list(self.main_categories.keys())

    def on_pre_enter(self):
        """画面遷移前にアプリケーション一覧を再読み込み"""
        self.load_applications()

        if self.selected_main_category_name:
            # 選択されているメインカテゴリ名があれば、サブカテゴリを更新
            self.update_sub_categories(self.selected_main_category_name)

    def update_sub_categories(self, selected_application_name):
        """選択されたアプリケーションに基づいてサブカテゴリを更新"""
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
                # 実行中でない場合、選択されたサブカテゴリをクリア
                self.selected_sub_category = ""

    def on_confirm(self):
        """確認ボタンが押されたときの処理"""
        if self.selected_client_id and self.selected_sub_category:
            if not self.is_running:
                self.show_presence(
                    self.selected_client_id, self.selected_sub_category
                )

                # ログを追加し、現在のログIDを保持
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

                    # ログの終了時間を更新
                    with session_scope() as session:
                        log_dao = LogDao(session)
                        log_dao.update_end_time(
                            self.current_log_id, datetime.now()
                        )
                        self.current_log_id = None

                self.is_running = False

    def go_to_subcategory_manager(self):
        """サブカテゴリ管理画面に遷移"""
        self.manager.current = "subcategory_manager"

    def show_presence(self, client_id, detail):
        """Discordのプレゼンスを表示"""
        if self.presence is None or self.presence.loop._closed:
            self.presence = Presence(client_id)
            self.presence.connect()
            self.presence.update(details=detail)

    def hide_presence(self):
        """Discordのプレゼンスを非表示"""
        if self.presence:
            self.presence.clear()
            self.presence.close()

    def go_to_discord_manager(self):
        """Discordアプリ管理画面に遷移"""
        self.manager.current = "discord_application_manager"
