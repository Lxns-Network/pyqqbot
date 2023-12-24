from typing import Callable, Dict, List, Coroutine

import functools
import aiohttp
import asyncio
import copy
import sys

from .models.ws import Intents, OpCode, Load, HeartBeat
from .event.enums import EventModel, EventBody, Event
from .event.models import Ready
from .entities.components.parser import MessageParser
from .entities import MessageComponent
from .protocol import QQBotProtocol, HttpClient, CosClient
from .logger import Network, Session, Event as EventLogger
from .misc import argument_signature


class QQBot(QQBotProtocol):
    http: HttpClient
    cos: CosClient
    event: Dict[
        str, List[Callable[[EventBody], Coroutine]]
    ] = {}

    def __init__(self, app_id: int, client_secret: str, intents: Intents = Intents.default()):
        super().__init__(app_id, client_secret)

        self.app_id = app_id
        self.client_secret = client_secret
        self.intents = intents.to_int()

        self._openapi_url = 'https://api.sgroup.qq.com'
        self._access_token = None
        self._session = None
        self._ws = None

        self._heartbeat_interval = None
        self._session_id = None
        self._s = 0

        self.queue = None

    def init_cos_client(self, region: str, secret_id: str, secret_key: str, bucket: str):
        self.cos = CosClient(region, secret_id, secret_key, bucket)

    def run(self, loop=None):
        loop = loop or asyncio.get_event_loop()
        self.queue = asyncio.Queue(loop=loop) if sys.version_info.minor < 10 else asyncio.Queue()
        loop.run_until_complete(self._run())

    async def _run(self):
        self._access_token = None

        if self._session is not None:
            await self._session.close()

        self._session = aiohttp.ClientSession()
        asyncio.create_task(self.access_token_refresh_loop())
        asyncio.create_task(self.event_loop())

        while self._access_token is None:
            await asyncio.sleep(1)

        gateway_url = await self._get_gateway_url()

        while True:
            try:
                self._ws = await self._session.ws_connect(gateway_url)
                await self.ws_event_loop()
            except aiohttp.ClientError:
                pass

    async def _auth(self):
        if self._session_id is None:
            load = Load(op=OpCode.Identify, d={
                'token': self._access_token,
                'intents': self.intents,
                'shard': [0, 1],
                'properties': {
                    '$os': 'linux',
                    '$browser': 'pyqqbot',
                    '$device': 'pyqqbot'
                }
            })
        else:
            load = Load(op=OpCode.Resume, d={
                'token': self._access_token,
                'session_id': self._session_id,
                'seq': self._s
            })

        await self._ws.send_json(load.dict())

    async def _heartbeat(self):
        while True:
            if not self._session.closed:
                await self._ws.send_json(Load(op=OpCode.Heartbeat, d=self._s).dict())
            
            await asyncio.sleep(self._heartbeat_interval)

    async def access_token_refresh_loop(self):
        while not self._session.closed:
            result = await self._get_app_access_token()
            self._access_token = f"QQBot {result.access_token}"
            self.http = HttpClient(self.app_id, self._access_token, self._openapi_url, self._session)
            await asyncio.sleep(result.expires_in - 60)

    async def ws_event_loop(self):
        while True:
            msg = await self._ws.receive()

            if msg.type == aiohttp.WSMsgType.TEXT:
                load = Load.parse_raw(msg.data)
                if load.op == OpCode.Hello:
                    d = HeartBeat.parse_obj(load.d)
                    self._heartbeat_interval = d.heartbeat_interval / 1000
                    await self._auth()
                elif load.op == OpCode.Dispatch:
                    self._s = load.s
                    if load.t == 'READY':
                        d = Ready.parse_obj(load.d)
                        self._session_id = d.session_id
                        Session.info(f'已连接: @{d.user.username} ({d.user.id})')
                        asyncio.create_task(self._heartbeat())
                    elif load.t == 'RESUMED':
                        Network.info('重连成功')

                    await self.register_event(load)
                elif load.op == OpCode.InvalidSession:
                    Session.error('鉴权失败，可能是事件订阅参数有误')
                    raise Exception('invalid session')
                elif load.op == OpCode.HeartbeatAck:
                    Network.info('收到心跳响应')
                elif load.op == OpCode.Reconnect:
                    Network.warn('收到重连请求')
                    break
            elif msg.type == aiohttp.WSMsgType.CLOSE:
                if msg.data == 4009:
                    Session.warn('连接超时，尝试重新登录')
                elif msg.data >= 4900:
                    Network.warn('内部错误，尝试重新登录')
                else:
                    continue

                break
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                Network.info('连接已关闭，尝试重新登录')
                break

    async def register_event(self, load: Load):
        """
        注册事件到事件队列
        :param load:
        :return:
        """
        event_class_name = self.get_event_class_name()

        event_type = load.t
        if event_type not in event_class_name:
            EventLogger.warn(f'接收到未知事件 {load.t}: {load.d}')
            return

        # 这里要把 client 传进去，因为有些事件需要用到 client
        event_body = event_class_name[event_type](client=self, **load.d)
        await self.queue.put(Event(name=event_type, body=event_body))

    async def event_loop(self):
        while not self._session.closed:
            try:
                event: Event = await asyncio.wait_for(self.queue.get(), 3)
            except asyncio.TimeoutError:
                continue

            place_annotation = self.get_annotations_mapping()

            for callback in self.event.get(event.name, []):
                call_params = {}

                for name, annotation, default in argument_signature(callback):
                    if annotation in place_annotation:
                        call_params[name] = place_annotation[annotation](event)

                asyncio.create_task(callback(**call_params))

    def add_event_handler(self, event_name: str, func: Callable):
        """
        添加事件监听器
        :param event_name:
        :param func:
        :return:
        """
        if event_name not in self.get_event_class_name():
            raise ValueError('未知监听事件: %s' % event_name)

        self.event.setdefault(event_name, [])
        self.event[event_name].append(func)

    def event_handler(self, event_name: str):
        def decorator(func):
            self.add_event_handler(event_name, func)
            return func

        return decorator

    @staticmethod
    def get_event_class_name():
        return {
            event_name: event_class.value for event_name, event_class in EventModel.__members__.items()
        }

    def get_annotations_mapping(self):
        return {
            QQBot: lambda event: self,
            List[MessageComponent]: lambda event: MessageParser(event.body.dict()).parse_dict(),
            **self.generate_event_annotation(),
        }

    @staticmethod
    def generate_event_annotation():
        def wrapper(name, event_context):
            if name != event_context.name:
                raise ValueError("cannot look up a non-listened event.")

            return event_context.body

        return {
            event_class.value: functools.partial(wrapper, copy.copy(event_name))
            for event_name, event_class in EventModel.__members__.items()
        }
