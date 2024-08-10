from datetime import datetime


from pydantic import BaseModel, ConfigDict, model_validator, field_validator


class ReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime


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
    model_config = ConfigDict(from_attributes=True)
