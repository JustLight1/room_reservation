from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Reservation(Base):
    """
    Модель бронирования переговорной комнаты.

    Inherits:
        Base: Базовый класс для всех моделей.
        Attributes:
            __tablename__ (str): Имя таблицы, устанавливается как имя класса
                                в нижнем регистре.
            id (Mapped[int]): Первичный ключ.

    Attributes:
        from_reserve (Mapped[DateTime]): Время начала бронирования.
        to_reserve (Mapped[DateTime]): Время окончания бронирования.
        meetingroom_id (Mapped[int]): Внешний ключ на переговорную комнату
                                      (Один-ко-многим).
        user_id (Mapped[int]): Внешний ключ на пользователя, сделавшего
                               бронирование (Один-ко-многим).
    """
    from_reserve: Mapped[DateTime] = mapped_column(DateTime)
    to_reserve: Mapped[DateTime] = mapped_column(DateTime)
    meetingroom_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('meetingroom.id')
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id')
    )

    def __repr__(self):
        return (
            f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
        )
