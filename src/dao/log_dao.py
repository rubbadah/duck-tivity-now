from sqlalchemy.orm import Session

from dao.base_dao import BaseDao
from models.log import Log


class LogDao(BaseDao):
    def __init__(self, session: Session):
        super().__init__(session)
        self.model = Log

    def add_log(
        self,
        detail_id: int,
    ) -> Log:
        new_log = Log(
            detail_id=detail_id,
        )
        self.session.add(new_log)
        self.session.commit()
        return new_log

    def get_log_by_id(self, log_id: int) -> Log:
        return (
            self.session.query(Log)
            .filter(Log.id == log_id, ~Log.is_deleted)
            .first()
        )

    def get_all_logs(self):
        query = self.session.query(Log)
        query = self._add_common_filters(query)
        return query.all()

    def update_end_time(self, log_id: int, end_time: str) -> None:
        log = self.get_log_by_id(log_id)
        if log:
            log.end_time = end_time
            self.session.commit()
