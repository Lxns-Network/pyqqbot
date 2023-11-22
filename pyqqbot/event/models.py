from pydantic import BaseModel

from ..entities import Bot


class EventBody(BaseModel):
    pass


class Ready(EventBody):
    version: int
    session_id: str
    user: Bot
    shard: list


class Resumed(EventBody):
    pass


class Event(BaseModel):
    name: str
    body: EventBody

    def __init__(self, name: str, body: EventBody):
        super().__init__(name=name, body=body)
        self.name = name
        self.body = body
