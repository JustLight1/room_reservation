from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Reservation(Base):
    from_reserve: Mapped[DateTime] = mapped_column(DateTime)
    to_reserve: Mapped[DateTime] = mapped_column(DateTime)
    meetingroom_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('meetingroom.id')
    )
