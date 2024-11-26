from sqlalchemy.orm import Session

from dao.base_dao import BaseDao
from models.discord_application import DiscordApplication


class DiscordApplicationDao(BaseDao):
    def __init__(self, session: Session):
        super().__init__(session)
        self.model = DiscordApplication

    def add_application(self, client_id: str, name) -> DiscordApplication:
        new_app = DiscordApplication(client_id=client_id, name=name)
        self.session.add(new_app)
        self.session.commit()
        return new_app

    def get_application_by_id(self, app_id: int) -> DiscordApplication:
        return (
            self.session.query(DiscordApplication)
            .filter(
                DiscordApplication.id == app_id, ~DiscordApplication.is_deleted
            )
            .first()
        )

    def get_all_applications(self):
        query = self.session.query(DiscordApplication)
        query = self._add_common_filters(query)
        return query.all()

    def update_application(
        self, app_id: int, client_id: str, name: str
    ) -> None:
        app = self.get_application_by_id(app_id)
        if app:
            app.client_id = client_id
            app.name = name
            self.session.commit()

    def logical_delete_by_client_id(self, client_id) -> None:

        data = (
            self.session.query(DiscordApplication)
            .filter(DiscordApplication.client_id == client_id)
            .first()
        )
        data.is_deleted = True

    def update_application_name(self, client_id: str, name: str):
        """アプリケーション名を更新

        Args:
            client_id (str): クライアントID
            name (str): 新しいアプリケーション名
        """
        app = (
            self.session.query(DiscordApplication)
            .filter_by(client_id=client_id)
            .first()
        )
        if app:
            app.name = name
            self.session.commit()
