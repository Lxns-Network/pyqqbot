from pydantic import BaseModel


class Bot(BaseModel):
    id: str
    username: str
    bot: bool
    status: int
