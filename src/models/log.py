from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from database import Base

from .mixins import FixedColumns, UTCToJSTType


class Log(Base, FixedColumns):
    """プリセンスの更新を蓄積するモデル"""

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    detail_id = Column(
        Integer, ForeignKey("details.id"), nullable=False, comment="詳細ID"
    )
    start_time = Column(
        UTCToJSTType,
        nullable=False,
        default=func.now(),
        comment="表示開始時間",
    )
    end_time = Column(DateTime, comment="表示終了時間")

    # リレーションの設定
    detail = relationship("Detail", backref="logs")
