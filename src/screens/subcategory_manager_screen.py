from kivy.app import App
from kivy.properties import (
    BooleanProperty,
    DictProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from dao import DetailDao
from database import session_scope


class SubcategoryManagerScreen(Screen):
    """サブカテゴリ管理画面"""

    sub_categories = DictProperty({})
    client_id = StringProperty("")
    new_subcategory = StringProperty("")

    def update_rv_data(self):
        """リストビューのデータを更新"""
        self.ids.rv.data = [
            {"text": content, "item_id": id, "subcategory_screen": self}
            for id, content in self.sub_categories.items()
        ]

    def on_pre_enter(self):
        """画面遷移前にMainScreenのsub_categoriesを同期"""
        main_screen = self.manager.get_screen("main")
        self.sub_categories = main_screen.sub_categories.copy()
        self.client_id = main_screen.selected_client_id
        self.update_rv_data()

    def on_leave(self):
        """画面を離れる際に編集したsub_categoriesをMainScreenに反映"""
        main_screen = self.manager.get_screen("main")
        main_screen.sub_categories = self.sub_categories.copy()

    def add_subcategory(self):
        """新しいサブカテゴリを追加"""
        new_sub = self.new_subcategory.strip()
        if new_sub:
            with session_scope() as session:
                detail_dao = DetailDao(session)
                new_detail = detail_dao.add_detail(new_sub, self.client_id)
                self.sub_categories[new_detail.id] = new_detail.content
            self.update_rv_data()
            # 入力フィールドをクリア
            self.new_subcategory = ""

    def go_back(self):
        """メイン画面に遷移"""
        self.manager.current = "main"


class SubcategoryItem(BoxLayout):
    """サブカテゴリアイテム"""

    text = StringProperty("")
    item_id = NumericProperty(-1)
    is_editing = BooleanProperty(False)
    is_selected = BooleanProperty(False)
    editing_subcategory = StringProperty("")
    subcategory_screen = ObjectProperty(None)

    def toggle_edit(self):
        """編集モードの切り替え"""
        if self.is_editing:
            # 編集モード確定
            self.confirm_edit(self.editing_subcategory)
        else:
            # 編集モードに入る
            self.editing_subcategory = self.text
            self.is_editing = True  # 編集モード開始

    def confirm_edit(self, new_text):
        """新しいテキストでサブカテゴリを更新"""
        if new_text.strip():
            with session_scope() as session:
                subcategory_item_dao = DetailDao(session)
                subcategory_item_dao.update_detail(self.item_id, new_text)
            self.text = new_text
            self.subcategory_screen.sub_categories[self.item_id] = new_text
            self.subcategory_screen.update_rv_data()
        self.is_editing = False  # 編集モード終了

    def delete_subcategory(self):
        """サブカテゴリを削除"""
        with session_scope() as session:
            subcategory_item_dao = DetailDao(session)
            subcategory_item_dao.logical_delete(self.item_id)
        del self.subcategory_screen.sub_categories[self.item_id]
        self.subcategory_screen.update_rv_data()
