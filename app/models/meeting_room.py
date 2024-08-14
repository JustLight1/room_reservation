from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


if TYPE_CHECKING:
    from app.models.reservation import Reservation


class MeetingRoom(Base):
    """
    Модель переговорной комнаты.

    Inherits:
        Base: Базовый класс для всех моделей.
        Attributes:
            __tablename__ (str): Имя таблицы, устанавливается как имя класса
                                в нижнем регистре.
            id (Mapped[int]): Первичный ключ.

    Attributes:
        name (Mapped[str]): Название переговорной комнаты.
        description (Mapped[str or None]): Описание переговорной комнаты.
        reservations (relationship): Связь с моделью бронирований.
    """
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    reservations: Mapped[list['Reservation']] = relationship(
        'Reservation', cascade='delete')
