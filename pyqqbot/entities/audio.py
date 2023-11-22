from pydantic import BaseModel


class AudioChannelMemberEvent(BaseModel):
    channel_id: str
    channel_type: int
    guild_id: str
    user_id: str


class AudioChannelMemberEnter(AudioChannelMemberEvent):
    pass


class AudioChannelMemberExit(AudioChannelMemberEvent):
    pass
