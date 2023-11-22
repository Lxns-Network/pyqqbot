from enum import Enum


class MessageType(Enum):
    TEXT = 0
    TEXT_WITH_IMAGE = 1
    MARKDOWN = 2
    ARK = 3
    EMBED = 4
    MEDIA = 7


class AttachmentType(Enum):
    IMAGE = 1
    VIDEO = 2
    VOICE = 3
    FILE = 4

