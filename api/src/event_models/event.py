from pydantic import BaseModel


class BaseEvent(BaseModel):
    topic: str
    key: str
    value: str
