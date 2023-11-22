from pydantic import BaseModel, validator
from typing import List, Union, Optional, Any

from pyqqbot.entities.components.parser import MessageParser
from pyqqbot.entities.components import MessageComponent
from .components import Attachment
from .enums import *


class GuildUser(BaseModel):
    avatar: Optional[str]
    bot: Optional[bool]
    id: str
    username: Optional[str]


class GuildMember(BaseModel):
    joined_at: str
    nick: Optional[str]
    roles: Optional[List[str]]


class GuildSimpleMessage(BaseModel):
    author: GuildUser
    channel_id: str
    guild_id: str
    id: str


class GuildMessage(BaseModel):
    """
    文字子频道@机器人
    """
    author: GuildUser
    channel_id: str
    content: Optional[str]
    guild_id: str
    id: str
    member: GuildMember
    mentions: List[GuildUser]
    seq: int
    seq_in_channel: str
    timestamp: str
    attachments: Optional[List[Attachment]]

    client: Any

    def __init__(self, client: Any, **data):
        super().__init__(**data)
        self.client = client

    async def reply(self, content: Union[str, List[MessageComponent]]):
        """
        发送消息到文字子频道
        :param content:
        :return:
        """
        if isinstance(content, list):
            message = MessageParser.to_dict(content)
        else:
            message = {'content': content}

        return await self.client.http.post(f'/channels/{self.channel_id}/messages', data={
            'msg_id': self.id,
            **message,
        })


class GuildFullMessage(GuildMessage):
    """
    文字子频道全量消息（私域）
    """
    pass


class GuildDirectMessage(BaseModel):
    """
    频道私信消息
    """
    author: GuildUser
    channel_id: str
    content: Optional[str]
    guild_id: str
    id: str
    member: GuildMember
    timestamp: str
    attachments: Optional[List[Attachment]]

    client: Any

    def __init__(self, client: Any, **data):
        super().__init__(**data)
        self.client = client

    async def reply(self, content: Union[str, List[MessageComponent]]):
        """
        发送消息到频道私信
        :param content:
        :return:
        """
        if isinstance(content, list):
            message = MessageParser.to_dict(content)
        else:
            message = {'content': content}

        return await self.client.http.post(f'/dms/{self.guild_id}/messages', data={
            'msg_id': self.id,
            **message,
        })


class GuildDeleteMessage(BaseModel):
    message: GuildSimpleMessage
    op_user: GuildUser


class Emoji(BaseModel):
    id: str
    type: int


class ReactionTarget(BaseModel):
    id: str
    type: str


class MessageReactionEvent(BaseModel):
    """
    表情表态基础事件
    """
    channel_id: str
    emoji: Emoji
    guild_id: str
    target: ReactionTarget
    user_id: str


class GuildAddMessageReaction(MessageReactionEvent):
    """
    用户对消息进行表情表态
    """
    pass


class GuildRemoveMessageReaction(MessageReactionEvent):
    """
    用户对消息进行取消表情表态
    """
    pass


class GuildMemberOperationEvent(BaseModel):
    """
    频道成员基础事件
    """
    guild_id: str
    joined_at: str
    nick: str
    op_user_id: str
    roles: List[str]
    user: GuildUser


class GuildAddMember(GuildMemberOperationEvent):
    """
    新用户加入频道
    """
    pass


class GuildUpdateMember(GuildMemberOperationEvent):
    """
    用户的频道属性发生变化
    """
    pass


class GuildRemoveMember(GuildMemberOperationEvent):
    """
    用户离开频道
    """
    pass


class GuildOperationEvent(BaseModel):
    """
    频道基础事件
    """
    description: str
    icon: str
    id: str
    joined_at: str
    max_members: int
    member_count: int
    name: str
    op_user_id: str
    owner: bool
    owner_id: str
    union_appid: str
    union_org_id: str
    union_world_id: str


class GuildCreate(GuildOperationEvent):
    """
    机器人被加入到某个频道
    """
    pass


class GuildUpdate(GuildOperationEvent):
    """
    频道信息变更
    """
    pass


class GuildRemove(GuildOperationEvent):
    """
    频道被解散或机器人被移除
    """
    pass


class GuildPermissions(BaseModel):
    """
    权限
    """
    access_channels: bool
    manage_channels: bool
    speak_in_channels: bool
    live_in_channels: bool

    @classmethod
    def from_int(cls, value: int):
        return cls(
            access_channels=bool(value & 1),
            manage_channels=bool(value & 2),
            speak_in_channels=bool(value & 3),
            live_in_channels=bool(value & 4),
        )


class GuildChannelOperationEvent(BaseModel):
    application_id: Optional[str]
    guild_id: str
    id: str
    name: str
    op_user_id: str
    owner_id: str
    parent_id: Optional[str]
    permissions: Optional[GuildPermissions]
    position: Optional[int]
    private_type: PrivateType
    speak_permission: SpeakPermission
    sub_type: ChannelSubType
    type: ChannelType

    @validator('permissions', pre=True)
    def permissions_from_str(cls, value: str):
        if not value:
            return None
        return GuildPermissions.from_int(int(value))


class GuildCreateChannel(GuildChannelOperationEvent):
    """
    子频道被创建
    """
    pass


class GuildUpdateChannel(GuildChannelOperationEvent):
    """
    子频道信息变更
    """
    pass


class GuildRemoveChannel(GuildChannelOperationEvent):
    """
    子频道被删除
    """
    pass
