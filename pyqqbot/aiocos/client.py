import logging
import aiohttp
from .reqrep import COSResponse, COSRequest
from .errors import CosServiceError
from .utils import *

logger = logging.getLogger(__name__)

__all__ = ['CosS3Client']


async def _parser_headers(resp):
    return dict(resp.headers)


async def _parser(resp):
    return await resp.text()


class CosS3Client:
    def __init__(self, config):
        self._config = config
        self.auth = config.get_auth()
        self._session = aiohttp.ClientSession(request_class=COSRequest,
                                              response_class=COSResponse,
                                              auth=self.auth)

    def _get_url(self, bucket, key=''):
        key = key.lstrip('/')
        url = 'https://%s.cos.%s.myqcloud.com/%s' % (bucket, self._config.region, key)
        return url

    async def _request(self, method, *args, parser=None, **kwargs):
        parser = parser or _parser
        try:
            async with self._session.request(method, *args, **kwargs) as resp:
                status = resp.status
                if status >= 400:
                    text = await resp.text()
                    raise CosServiceError(text, status)
                result = parser(resp)
                while isawaitable(result):
                    result = await result
                return result
        except CosServiceError:
            raise
        except Exception as e:
            raise CosClientError from e

    async def put_object(self, Bucket, Body, Key, EnableMD5=False, **kwargs):
        await check_object_content_length(Body)
        headers = mapped(kwargs)
        url = self._get_url(Bucket, Key)
        if EnableMD5:
            md5_str = await get_content_md5(Body)
            if md5_str is not None:
                headers['Content-MD5'] = md5_str
        return await self._request('PUT', url=url, data=Body, headers=headers, parser=_parser_headers)

    async def delete_object(self, Bucket, Key, **kwargs):
        headers = mapped(kwargs)
        params = {}
        if 'versionId' in headers:
            params['versionId'] = headers['versionId']
            del headers['versionId']
        url = self._get_url(Bucket, Key)
        logger.info("delete object, url=:{url} ,headers=:{headers}".format(
            url=url,
            headers=headers))
        return await self._request('DELETE', url=url, parser=_parser_headers, headers=headers, params=params)

    def get_auth(self, Method, Bucket, Key, Expired=300, Headers=None, Params=None):
        region = self._config.region
        Headers = Headers or {}
        if 'Host' not in Headers:
            Headers.add('Host', '%s.cos.%s.myqcloud.com' % (Bucket, region))
        return self.auth.get_auth(Method, Key, Expired, Headers, Params or {})
