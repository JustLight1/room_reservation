from typing import TYPE_CHECKING, List

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


if TYPE_CHECKING:
    from app.models.reservation import Reservation


class MeetingRoom(Base):
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    reservations: Mapped[List['Reservation']] = relationship(
        'Reservation', cascade='delete')
