from fastapi import FastAPI

from app.core.config import settings
from app.api.meeting_room import router as router_meeting_room


app = FastAPI(title=settings.app_title)

app.include_router(router_meeting_room)
