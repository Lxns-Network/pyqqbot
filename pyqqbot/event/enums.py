from enum import Enum

from ..entities import *
from .models import *


class EventModel(Enum):
    """
    事件模型
    """
    READY = Ready
    RESUMED = Resumed

    C2C_MESSAGE_CREATE = DirectMessage
    FRIEND_ADD = UserAddBot
    FRIEND_DEL = UserRemoveBot
    C2C_MSG_REJECT = UserRejectBotMessage
    C2C_MSG_RECEIVE = UserReceiveBotMessage

    GROUP_AT_MESSAGE_CREATE = GroupMessage
    GROUP_ADD_ROBOT = GroupAddBot
    GROUP_DEL_ROBOT = GroupRemoveBot
    GROUP_MSG_REJECT = GroupRejectBotMessage
    GROUP_MSG_RECEIVE = GroupReceiveBotMessage

    AT_MESSAGE_CREATE = GuildMessage
    DIRECT_MESSAGE_CREATE = GuildDirectMessage
    MESSAGE_CREATE = GuildFullMessage
    PUBLIC_MESSAGE_DELETE = GuildDeleteMessage
    MESSAGE_REACTION_ADD = GuildAddMessageReaction
    MESSAGE_REACTION_REMOVE = GuildRemoveMessageReaction

    GUILD_CREATE = GuildCreate
    GUILD_UPDATE = GuildUpdate
    GUILD_DELETE = GuildRemove
    CHANNEL_CREATE = GuildCreateChannel
    CHANNEL_UPDATE = GuildUpdateChannel
    CHANNEL_DELETE = GuildRemoveChannel
    GUILD_MEMBER_ADD = GuildAddMember
    GUILD_MEMBER_UPDATE = GuildUpdateMember
    GUILD_MEMBER_REMOVE = GuildRemoveMember

    OPEN_FORUM_POST_CREATE = ForumCreatePost
    OPEN_FORUM_THREAD_CREATE = ForumCreateThread
    OPEN_FORUM_THREAD_UPDATE = ForumUpdateThread
    OPEN_FORUM_THREAD_DELETE = ForumRemoveThread
    OPEN_FORUM_REPLY_CREATE = ForumCreateReply

    AUDIO_OR_LIVE_CHANNEL_MEMBER_ENTER = AudioChannelMemberEnter
    AUDIO_OR_LIVE_CHANNEL_MEMBER_EXIT = AudioChannelMemberExit


class EventType(Enum):
    """
    事件类型
    """
    READY = 'READY'
    RESUMED = 'RESUMED'

    # 单聊
    C2C_MESSAGE_CREATE = 'C2C_MESSAGE_CREATE'
    FRIEND_ADD = 'FRIEND_ADD'
    FRIEND_DEL = 'FRIEND_DEL'
    C2C_MSG_REJECT = 'C2C_MSG_REJECT'
    C2C_MSG_RECEIVE = 'C2C_MSG_RECEIVE'

    # 群聊
    GROUP_AT_MESSAGE_CREATE = 'GROUP_AT_MESSAGE_CREATE'
    GROUP_ADD_ROBOT = 'GROUP_ADD_ROBOT'
    GROUP_DEL_ROBOT = 'GROUP_DEL_ROBOT'
    GROUP_MSG_REJECT = 'GROUP_MSG_REJECT'
    GROUP_MSG_RECEIVE = 'GROUP_MSG_RECEIVE'

    # 频道
    AT_MESSAGE_CREATE = 'AT_MESSAGE_CREATE'
    DIRECT_MESSAGE_CREATE = 'DIRECT_MESSAGE_CREATE'
    MESSAGE_CREATE = 'MESSAGE_CREATE'  # 仅私域
    PUBLIC_MESSAGE_DELETE = 'PUBLIC_MESSAGE_DELETE'
    MESSAGE_REACTION_ADD = 'MESSAGE_REACTION_ADD'
    MESSAGE_REACTION_REMOVE = 'MESSAGE_REACTION_REMOVE'

    # 频道管理
    GUILD_CREATE = 'GUILD_CREATE'
    GUILD_UPDATE = 'GUILD_UPDATE'
    GUILD_DELETE = 'GUILD_DELETE'
    CHANNEL_CREATE = 'CHANNEL_CREATE'
    CHANNEL_UPDATE = 'CHANNEL_UPDATE'
    CHANNEL_DELETE = 'CHANNEL_DELETE'
    GUILD_MEMBER_ADD = 'GUILD_MEMBER_ADD'
    GUILD_MEMBER_UPDATE = 'GUILD_MEMBER_UPDATE'
    GUILD_MEMBER_REMOVE = 'GUILD_MEMBER_REMOVE'

    # 频道论坛
    OPEN_FORUM_POST_CREATE = 'OPEN_FORUM_POST_CREATE'
    OPEN_FORUM_THREAD_CREATE = 'OPEN_FORUM_THREAD_CREATE'
    OPEN_FORUM_THREAD_UPDATE = 'OPEN_FORUM_THREAD_UPDATE'
    OPEN_FORUM_THREAD_DELETE = 'OPEN_FORUM_THREAD_DELETE'
    OPEN_FORUM_REPLY_CREATE = 'OPEN_FORUM_REPLY_CREATE'

    # 频道语音
    AUDIO_OR_LIVE_CHANNEL_MEMBER_ENTER = 'AUDIO_OR_LIVE_CHANNEL_MEMBER_ENTER'
    AUDIO_OR_LIVE_CHANNEL_MEMBER_EXIT = 'AUDIO_OR_LIVE_CHANNEL_MEMBER_EXIT'