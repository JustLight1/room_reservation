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
    """
    Базовая схема бронирования.

    Attributes:
        from_reserve (dt.datetime): Время начала бронирования.
        to_reserve (dt.datetime): Время окончания бронирования.
        model_config (ConfigDict): Конфигурация модели для запрета
        дополнительных полей при валидации.
    """
    from_reserve: datetime = Field(..., examples=[FROM_TIME])
    to_reserve: datetime = Field(..., examples=[TO_TIME])

    model_config = ConfigDict(extra='forbid')


class ReservationUpdate(ReservationBase):
    """
    Схема для обновления бронирования.

    Inherits:
        ReservationBase: Базовая схема бронирования.
    """

    @field_validator('from_reserve')
    @classmethod
    def check_from_reserve_later_than_now(cls, value):
        """
        Валидатор, проверяющий, что начало бронирования не меньше
        текущего времени.
        """
        if value <= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    @model_validator(mode='after')
    def check_from_reserve_before_to_reserve(self):
        """
        Валидатор, проверяющий, что время начала бронирования меньше
        времени окончания.
        """
        if self.from_reserve >= self.to_reserve:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return self


class ReservationCreate(ReservationUpdate):
    """
    Схема для создания нового бронирования.

    Inherits:
        ReservationUpdate: Модель для обновления бронирования.

    Attributes:
        meetingroom_id (int): Идентификатор переговорной комнаты.
    """
    meetingroom_id: int


class ReservationDB(ReservationBase):
    """
    Схема бронирования в базе данных.

    Inherits:
        ReservationBase: Базовая схема бронирования.

    Attributes:
        id (int): Идентификатор бронирования.
        meetingroom_id (int): Идентификатор переговорной комнаты.
        user_id (int): Идентификатор пользователя, создавшего бронирование.
        model_config (ConfigDict): Конфигурация схемы для сериализации объектов
        базы данных, а не только Python-словарь или JSON-объект.
    """
    id: int
    meetingroom_id: int
    user_id: int | None
    model_config = ConfigDict(from_attributes=True)
