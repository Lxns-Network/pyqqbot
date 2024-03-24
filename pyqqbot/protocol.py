from typing import Union, List

import aiohttp
import asyncio
import base64
import json

from .entities.components import MessageType
from .entities import Attachment, DirectMessage, MessageComponent, MessageParser, GroupMessage
from .models.api import *


class HttpClient:
    app_id: int

    _access_token: str | None
    _openapi_url: str
    _session: aiohttp.ClientSession | None

    def __init__(self, app_id: int, access_token: str, openapi_url: str, session: aiohttp.ClientSession):
        self.app_id = app_id
        self._access_token = access_token
        self._openapi_url = openapi_url
        self._session = session

    async def request(self, method, endpoint, params=None, data=None) -> dict:
        async with self._session.request(method, f'{self._openapi_url}{endpoint}', params=params, data=data, headers={
            'Authorization': self._access_token,
            'X-Union-Appid': str(self.app_id),
            'Content-Type': 'application/json'
        }) as resp:
            print(await resp.text())
            resp.raise_for_status()
            return await resp.json()

    async def get(self, endpoint, params=None) -> dict:
        return await self.request('GET', endpoint, params=params)

    async def post(self, endpoint, data=None) -> dict:
        return await self.request('POST', endpoint, data=json.dumps(data))


class QQBotProtocol:
    http: HttpClient
    app_id: int
    client_secret: str

    _access_token: str | None
    _openapi_url: str
    _session: aiohttp.ClientSession | None

    def __init__(self, app_id: int, client_secret: str):
        self.app_id = app_id
        self.client_secret = client_secret

        self._access_token = None
        self._openapi_url = 'https://api.sgroup.qq.com'
        self._session = None

    async def _get_app_access_token(self) -> GetAppAccessTokenResponse:
        """
        获取接口凭证
        :return:
        """
        async with self._session.post('https://bots.qq.com/app/getAppAccessToken', headers={
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'appId': str(self.app_id),
            'clientSecret': self.client_secret
        })) as resp:
            resp.raise_for_status()
            result = await resp.json()
            return GetAppAccessTokenResponse(**result)

    async def _get_gateway_url(self) -> str:
        """
        获取通用 WSS 接入点
        :return:
        """
        result = await self.http.get('/gateway')
        return result['url']

    async def send_c2c_message(self, source: DirectMessage,
                               content: Union[str, MessageComponent, List[MessageComponent]]) -> SendMessageResponse:
        """
        发送单聊消息
        :param source:
        :param content:
        :return:
        """
        if isinstance(content, MessageComponent):
            content = [content]

        if isinstance(content, list):
            message = MessageParser.to_dict(content)

            for i, component in enumerate(content):
                if isinstance(component, Attachment):
                    media = await self.upload_c2c_media_file(source.author.member_openid, attachment=component)
                    message['media'] = media.dict()
                    message['msg_type'] = MessageType.MEDIA.value
        else:
            message = {'content': content}

        result = await self.http.post(f'/v2/users/{source.author.member_openid}/messages', data={
            'msg_id': source.id,
            'msg_type': MessageType.TEXT.value,
            'msg_seq': source.msg_seq,
            **message,
        })
        return SendMessageResponse(**result)

    async def send_group_message(self, source: GroupMessage,
                                 content: Union[str, MessageComponent, List[MessageComponent]]) -> SendMessageResponse:
        """
        发送群聊消息
        :param source:
        :param content:
        :return:
        """
        if isinstance(content, MessageComponent):
            content = [content]

        if isinstance(content, list):
            message = MessageParser.to_dict(content)

            for i, component in enumerate(content):
                if isinstance(component, Attachment):
                    media = await self.upload_group_media_file(source.group_openid, attachment=component)
                    message['media'] = media.dict()
                    message['msg_type'] = MessageType.MEDIA.value
        else:
            message = {'content': content}

        result = await self.http.post(f'/v2/groups/{source.group_openid}/messages', data={
            'msg_id': source.id,
            'msg_type': MessageType.TEXT.value,
            'msg_seq': source.msg_seq,
            **message,
        })
        return SendMessageResponse(**result)

    async def _upload_media_file(self, endpoint: str, data: dict) -> UploadMediaFileResponse:
        """
        上传富媒体文件
        :param endpoint:
        :param data:
        :return:
        """
        result = await self.http.post(endpoint, data=data)
        return UploadMediaFileResponse(**result)

    async def upload_c2c_media_file(self, openid: str, url: str = None, attachment: Attachment = None,
                                    srv_send_msg: bool = False) -> UploadMediaFileResponse:
        """
        上传单聊富媒体文件
        :param openid:
        :param url:
        :param attachment:
        :param srv_send_msg:
        :return:
        """
        data = {
            'file_type': attachment.type.value,
            'srv_send_msg': srv_send_msg,
        }

        if url is not None:
            data['url'] = url
        elif attachment is not None:
            data['file_data'] = base64.b64encode(attachment.file).decode()
        else:
            raise ValueError('url 和 attachment 不能同时为空')

        return await self._upload_media_file(f'/v2/users/{openid}/files', {
            'file_type': attachment.type.value,
            'url': url,
            'srv_send_msg': srv_send_msg,
        })

    async def upload_group_media_file(self, group_openid: str, url: str = None, attachment: Attachment = None,
                                      srv_send_msg: bool = False) -> UploadMediaFileResponse:
        """
        上传群聊富媒体文件
        :param group_openid:
        :param url:
        :param attachment:
        :param srv_send_msg:
        :return:
        """
        data = {
            'file_type': attachment.type.value,
            'srv_send_msg': srv_send_msg,
        }

        if url is not None:
            data['url'] = url
        elif attachment is not None:
            data['file_data'] = base64.b64encode(attachment.file).decode()
        else:
            raise ValueError('url 和 attachment 不能同时为空')

        return await self._upload_media_file(f'/v2/groups/{group_openid}/files', data)
