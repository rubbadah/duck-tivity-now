from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

from .mixins import FixedColumns


class Detail(Base, FixedColumns):
    """詳細"""

    __tablename__ = "details"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    content = Column(String(100), nullable=False, comment="内容")
    client_id = Column(
        String(50),
        ForeignKey("discord_applications.client_id"),
        nullable=False,
        comment="クライアントID",
    )

    # リレーションの設定
    main_category = relationship("DiscordApplication")
