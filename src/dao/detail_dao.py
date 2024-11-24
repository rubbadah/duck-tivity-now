from sqlalchemy import and_
from sqlalchemy.orm import Session

from dao.base_dao import BaseDao
from models.detail import Detail


class DetailDao(BaseDao):
    def __init__(self, session: Session):
        super().__init__(session)
        self.model = Detail

    def add_detail(
        self,
        content: str,
        client_id: str,
    ) -> Detail:
        new_detail = Detail(
            content=content,
            client_id=client_id,
        )
        self.session.add(new_detail)
        self.session.commit()
        return new_detail

    def get_detail_by_id(self, detail_id: int) -> Detail:
        return (
            self.session.query(Detail)
            .filter(Detail.id == detail_id, ~Detail.is_deleted)
            .first()
        )

    def get_all_details(self):
        query = self.session.query(Detail)
        query = self._add_common_filters(query)
        return query.all()

    def update_detail(
        self,
        detail_id: int,
        content: str,
    ) -> None:
        detail = self.get_detail_by_id(detail_id)
        if detail:
            detail.content = content
            self.session.commit()

    def get_detail_by_client_id(self, client_id: str):
        query = self.session.query(Detail)
        query = self._add_common_filters(query)
        return query.filter(Detail.client_id == client_id).all()

    def logical_delete_by_name(self, client_id: str, name: str) -> None:

        data = (
            self.session.query(Detail)
            .filter(Detail.client_id == client_id and Detail.name == name)
            .first()
        )
        data.is_deleted = True
