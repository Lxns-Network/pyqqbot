from pydantic import BaseModel, validator
from typing import Optional

from .enums import *


class MessageComponent(BaseModel):
    def __str__(self):
        raise NotImplementedError


class Plain(MessageComponent):
    content: str

    def __init__(self, content: str):
        super().__init__(content=content)

    def __str__(self):
        return self.content


class At(MessageComponent):
    id: str

    def __init__(self, id: str):
        super().__init__(id=id)

    def __str__(self):
        return f'<@!{self.id}>'


class Attachment(MessageComponent):
    id: Optional[str]
    content_type: Optional[str]
    filename: str
    height: Optional[int]
    width: Optional[int]
    size: Optional[int]
    url: Optional[str]

    file: Optional[bytes]
    type: Optional[AttachmentType]

    @validator('url')
    def url_validator(cls, v):
        if not v.startswith('https://') and not v.startswith('http://'):
            return 'https://' + v
        return v

    def __str__(self):
        return None


class Image(Attachment):
    type: Optional[AttachmentType] = AttachmentType.IMAGE

    @staticmethod
    def from_local_storage(path: str):
        filename = path.split('/')[-1]

        with open(path, 'rb') as f:
            file = f.read()

        return Image(file=file, filename=filename)

    @staticmethod
    def from_bytes(file: bytes, filename: str):
        return Image(file=file, filename=filename)


class Video(Attachment):
    type: Optional[AttachmentType] = AttachmentType.VIDEO

    @staticmethod
    def from_local_storage(path: str):
        filename = path.split('/')[-1]

        with open(path, 'rb') as f:
            file = f.read()

        return Video(file=file, filename=filename)


class Voice(Attachment):
    type: Optional[AttachmentType] = AttachmentType.VOICE

    @staticmethod
    def from_local_storage(path: str):
        filename = path.split('/')[-1]

        with open(path, 'rb') as f:
            file = f.read()

        return Voice(file=file, filename=filename)


class File(Attachment):
    type: Optional[AttachmentType] = AttachmentType.FILE

    @staticmethod
    def from_local_storage(path: str):
        filename = path.split('/')[-1]

        with open(path, 'rb') as f:
            file = f.read()

        return File(file=file, filename=filename)
