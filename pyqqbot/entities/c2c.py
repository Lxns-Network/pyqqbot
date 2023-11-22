from pydantic import BaseModel
from typing import List, Union, Any

from .components import MessageComponent


class User(BaseModel):
    id: str
    member_openid: str


class DirectMessage(BaseModel):
    """
    单聊消息
    """
    author: User
    content: str
    id: str
    timestamp: str

    client: Any
    msg_seq: int = 0

    def __init__(self, client: Any, **data):
        super().__init__(**data)
        self.client = client

    async def reply(self, content: Union[str, MessageComponent, List[MessageComponent]]):
        """
        回复消息
        :param content:
        :return:
        """
        self.msg_seq += 1
        return await self.client.send_c2c_message(self, content)


class BaseUserOperationEvent(BaseModel):
    """
    用户管理基础事件
    """
    timestamp: int
    openid: str


class UserAddBot(BaseUserOperationEvent):
    """
    用户添加机器人
    """
    pass


class UserRemoveBot(BaseUserOperationEvent):
    """
    用户移除机器人
    """
    pass


class UserRejectBotMessage(BaseUserOperationEvent):
    """
    拒绝机器人主动消息
    """
    pass


class UserReceiveBotMessage(BaseUserOperationEvent):
    """
    允许机器人主动消息
    """
    pass
