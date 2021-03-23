from fastapi import APIRouter, Depends
from event_services.event import get_event_service, EventService
from event_models.event import BaseEvent
from api.v1.models import EventResp

router = APIRouter()


@router.post('/send_event/', response_model=EventResp)
async def event(event: BaseEvent, event_service: EventService = Depends(get_event_service)) -> EventResp:
    result = await event_service.send_event(event.topic, event.key, event.value)
    response = EventResp(success=result)
    return response
