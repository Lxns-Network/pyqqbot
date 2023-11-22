from enum import Enum


class ChannelType(Enum):
    """
    子频道类型
    """
    TEXT = 0
    UNKNOWN = 1
    VOICE = 2
    UNKNOWN_2 = 3
    SUB_CHANNEL_GROUP = 4
    LIVE = 10005
    APPLICATION = 10006
    FORUM = 10007


class ChannelSubType(Enum):
    """
    子频道子类型
    """
    TEXT = 0
    ANNOUNCEMENT = 1
    TIPS = 2
    GANG_UP = 3


class PrivateType(Enum):
    """
    子频道私密类型
    """
    PUBLIC = 0
    ADMIN = 1
    ADMIN_AND_SPECIFIC_USER = 2


class SpeakPermission(Enum):
    """
    子频道发言权限
    """
    INVALID = 0
    ALL = 1
    ADMIN_AND_SPECIFIC_USER = 2
