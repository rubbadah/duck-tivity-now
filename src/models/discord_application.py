from sqlalchemy import Column, Integer, String

from database import Base

from .mixins import FixedColumns


class DiscordApplication(Base, FixedColumns):
    """Discordアプリケーション"""

    __tablename__ = "discord_applications"

    client_id = Column(String(50), primary_key=True, comment="クライアントID")
    name = Column(String(100), comment="アプリケーション名")
