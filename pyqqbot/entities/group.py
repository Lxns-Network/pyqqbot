from pydantic import BaseModel
from typing import List, Optional, Union, Any

from .components import Attachment, MessageComponent
from .c2c import User


class GroupMessage(BaseModel):
    """
    群聊@机器人
    """
    author: User
    content: Optional[str]
    group_id: str
    group_openid: str
    id: str
    timestamp: str
    attachments: Optional[List[Attachment]]

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
        return await self.client.send_group_message(self, content)


class GroupOperationEvent(BaseModel):
    """
    群管理基础事件
    """
    timestamp: int
    group_openid: str
    op_member_openid: str


class GroupAddBot(GroupOperationEvent):
    """
    机器人加入群聊
    """
    pass


class GroupRemoveBot(GroupOperationEvent):
    """
    机器人退出群聊
    """
    pass


class GroupRejectBotMessage(GroupOperationEvent):
    """
    群聊拒绝机器人主动消息
    """
    pass


class GroupReceiveBotMessage(GroupOperationEvent):
    """
    群聊接收机器人主动消息
    """
    pass
