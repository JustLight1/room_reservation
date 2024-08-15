from pydantic import BaseModel, ConfigDict, Field, field_validator


class MeetingRoomBase(BaseModel):
    """
    Базовая схема переговорной комнаты.

    Attributes:
        name (str or None): Имя переговорной комнаты.
        description (str or None): Описание переговорной комнаты.
    """
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None


class MeetingRoomCreate(MeetingRoomBase):
    """
    Схема для создания новой переговорной комнаты.

    Attributes:
        name (str): Имя переговорной комнаты.
    """
    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomUpdate(MeetingRoomBase):
    """
    Схема для обновления переговорной комнаты.
    """

    @field_validator('name')
    @classmethod
    def name_cannot_be_null(cls, value):
        """
        Валидатор, проверяющий, что имя комнаты не может быть пустым.
        """
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


class MeetingRoomDB(MeetingRoomCreate):
    """
    Схема переговорной комнаты в базе данных.

    Inherits:
        MeetingRoomCreate: Схема для создания новой переговорной комнаты.

    Attributes:
        id (int): Идентификатор переговорной комнаты.
        model_config (ConfigDict): Конфигурация схемы для сериализации объектов
        базы данных, а не только Python-словарь или JSON-объект.
    """
    id: int
    model_config = ConfigDict(from_attributes=True)
