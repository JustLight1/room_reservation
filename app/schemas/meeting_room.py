from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomUpdate(MeetingRoomBase):

    @field_validator('name')
    @classmethod
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


class MeetingRoomDB(MeetingRoomCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
