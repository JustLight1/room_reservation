from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Reservation, User
from app.schemas.reservation import ReservationCreate, ReservationUpdate


class CRUDReservation(CRUDBase[
    Reservation,
    ReservationCreate,
    ReservationUpdate,
]):
    """
    Класс для операций CRUD с моделью Reservation.
    """

    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            reservation_id: int | None = None,
            session: AsyncSession,
    ) -> list[Reservation]:
        """
        Получает бронирования, происходящие в указанный период времени.

        Args:
            from_reserve (datetime): Время начала бронирования.
            to_reserve (datetime): Время окончания бронирования.
            meetingroom_id (int): Идентификатор переговорной комнаты.
            reservation_id (int or None, default = None): Идентификатор
                            бронирования (для исключения при поиске).
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            list[Reservation]: Список бронирований, происходящих в
                                   указанный период.
        """

        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession
    ) -> list[Reservation]:
        """
        Получает будущие бронирования для комнаты.

        Args:
            room_id (int): Идентификатор переговорной комнаты.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            list[Reservation]: Список будущих бронирований для указанной
                               комнаты.
        """
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User,
    ) -> list[Reservation]:
        """
        Получает бронирования, сделанные пользователем.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            user (User): Пользователь, чьи бронирования необходимо получить.

        Returns:
            list[Reservation]: Список бронирований, сделанных указанным
                               пользователем.
        """
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id
            )
        )
        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
