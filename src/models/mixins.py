from datetime import datetime, timedelta, timezone

from sqlalchemy import Boolean, Column, DateTime, func
from sqlalchemy.types import DateTime, TypeDecorator

JST = timezone(timedelta(hours=+9))


# def utc_to_jst(utc_dt):
#     return utc_dt.replace(tzinfo=timezone.utc).astimezone(JST)


# def jst_to_utc(jst_dt):
#     return jst_dt.replace(tzinfo=JST).astimezone(timezone.utc)


class UTCToJSTType(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.replace(tzinfo=JST).astimezone(
                timezone.utc
            )  # JSTをUTCに変換して保存

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.replace(tzinfo=timezone.utc).astimezone(
                JST
            )  # UTCをJSTに変換して返す


class FixedColumns(object):
    """全モデル共通のカラム定義"""

    is_deleted = Column(
        Boolean, default=False, nullable=False, comment="削除済"
    )
    created_at = Column(
        UTCToJSTType, default=func.now(), nullable=False, comment="作成日時"
    )
    updated_at = Column(
        UTCToJSTType,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="更新日時",
    )
