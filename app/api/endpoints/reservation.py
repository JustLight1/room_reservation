from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.reservation import reservation_crud
from app.api.validators import (
    check_meeting_room_exists,
    check_reservation_before_edit,
    check_reservation_intersections,
)
from app.schemas.reservation import (
    ReservationCreate, ReservationDB, ReservationUpdate
)
from app.core.user import current_user
from app.models import User


router = APIRouter()


@router.get('/', response_model=list[ReservationDB])
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session)
):
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.post('/', response_model=ReservationDB)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    await check_reservation_intersections(
        **reservation.model_dump(), session=session
    )
    new_reservation = await reservation_crud.create(
        reservation, session, user
    )
    return new_reservation


@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(
        reservation_id, session
    )
    await check_reservation_intersections(
        **obj_in.model_dump(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        obj_in=obj_in,
        session=session
    )
    return reservation


@router.delete('/{reservation_id}', response_model=ReservationDB)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(
        reservation_id, session
    )
    reservation = await reservation_crud.remove(
        reservation, session
    )
    return reservation
