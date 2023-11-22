from typing import List

import re

from . import *


class MessageParser:
    _message: dict

    content: str
    attachments: str

    _file_image: str

    def __init__(self, message: dict = None):
        self._message = message

    def parse_dict(self) -> List[MessageComponent]:
        """
        解析消息，返回消息组件列表
        """
        components = []

        for key, value in self._message.items():
            if value is None:
                continue

            if key == 'content':
                for match in re.findall(r'([\s\S]*)|<@!(\d+)>', value):
                    if match[0] and match[0] != '':
                        components.append(Plain(match[0]))
                    elif match[1]:
                        components.append(At(match[1]))
            elif key == 'attachments':
                for attachment in value:
                    if attachment['content_type'].startswith('image'):
                        components.append(Image.parse_obj(attachment))

        return components

    @staticmethod
    def to_dict(components: List[MessageComponent]) -> dict:
        """
        将消息组件列表转换为消息字典
        """
        message = {
            'content': '',
        }

        for component in components:
            if isinstance(component, (Plain, At)):
                message['content'] += str(component)
            elif isinstance(component, Image):
                if component.url:
                    message['image'] = component.url

        message['content'] = message['content'].strip()

        return message
