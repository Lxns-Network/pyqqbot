from pydantic import BaseModel


class ForumOperationEvent(BaseModel):
    author_id: str
    channel_id: str
    guild_id: str


class ForumCreatePost(ForumOperationEvent):
    pass


class ForumCreateThread(ForumOperationEvent):
    pass


class ForumUpdateThread(ForumOperationEvent):
    pass


class ForumRemoveThread(ForumOperationEvent):
    pass


class ForumCreateReply(ForumOperationEvent):
    pass
