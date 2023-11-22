from pydantic import BaseModel
from typing import Optional, Union


class HeartBeat(BaseModel):
    heartbeat_interval: int


class Load(BaseModel):
    op: int
    s: Optional[int]
    t: Optional[str]
    id: Optional[str]
    d: Optional[Union[dict, int]]

    def __init__(
        self,
        op: int,
        s: Optional[int] = None,
        t: Optional[str] = None,
        id: Optional[str] = None,
        d: Optional[Union[dict, int]] = None
    ):
        super().__init__(op=op, s=s, t=t, id=id, d=d)
