from datetime import datetime, timedelta

from pydantic import (BaseModel, ConfigDict, Field, model_validator,
                      field_validator)


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')
TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., examples=[FROM_TIME])
    to_reserve: datetime = Field(..., examples=[TO_TIME])

    model_config = ConfigDict(extra='forbid')


class ReservationUpdate(ReservationBase):

    @field_validator('from_reserve')
    @classmethod
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    @model_validator(mode='after')
    def check_from_reserve_before_to_reserve(self):
        if self.from_reserve >= self.to_reserve:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return self


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int
    user_id: int | None
    model_config = ConfigDict(from_attributes=True)
