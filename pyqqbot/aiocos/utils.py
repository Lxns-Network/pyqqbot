from urllib.parse import quote
from inspect import isawaitable
from hashlib import md5
import os
import re
from collections import defaultdict

from .errors import CosClientError

SINGLE_UPLOAD_LENGTH = 5 * 1024 * 1024 * 1024

map_list = {
    'ContentLength': 'Content-Length',
    'ContentMD5': 'Content-MD5',
    'ContentType': 'Content-Type',
    'CacheControl': 'Cache-Control',
    'ContentDisposition': 'Content-Disposition',
    'ContentEncoding': 'Content-Encoding',
    'ContentLanguage': 'Content-Language',
    'Expires': 'Expires',
    'ResponseContentType': 'response-content-type',
    'ResponseContentLanguage': 'response-content-language',
    'ResponseExpires': 'response-expires',
    'ResponseCacheControl': 'response-cache-control',
    'ResponseContentDisposition': 'response-content-disposition',
    'ResponseContentEncoding': 'response-content-encoding',
    'Metadata': 'Metadata',
    'ACL': 'x-cos-acl',
    'GrantFullControl': 'x-cos-grant-full-control',
    'GrantWrite': 'x-cos-grant-write',
    'GrantRead': 'x-cos-grant-read',
    'StorageClass': 'x-cos-storage-class',
    'Range': 'Range',
    'IfMatch': 'If-Match',
    'IfNoneMatch': 'If-None-Match',
    'IfModifiedSince': 'If-Modified-Since',
    'IfUnmodifiedSince': 'If-Unmodified-Since',
    'CopySourceIfMatch': 'x-cos-copy-source-If-Match',
    'CopySourceIfNoneMatch': 'x-cos-copy-source-If-None-Match',
    'CopySourceIfModifiedSince': 'x-cos-copy-source-If-Modified-Since',
    'CopySourceIfUnmodifiedSince': 'x-cos-copy-source-If-Unmodified-Since',
    'VersionId': 'versionId',
    'ServerSideEncryption': 'x-cos-server-side-encryption',
    'SSECustomerAlgorithm': 'x-cos-server-side-encryption-customer-algorithm',
    'SSECustomerKey': 'x-cos-server-side-encryption-customer-key',
    'SSECustomerKeyMD5': 'x-cos-server-side-encryption-customer-key-MD5',
    'SSEKMSKeyId': 'x-cos-server-side-encryption-cos-kms-key-id'
}


class CosConfig:
    def __init__(self, SecretId, SecretKey, Region, Token=''):
        self.secret_id = SecretId
        self.secret_key = SecretKey
        self.region = Region
        self.token = Token
        self.expire = 100

    def get_auth(self):
        from .auth import Auth
        return Auth(self.secret_id, self.secret_key, self.expire)


def ensure_bytes(s):
    if type(s) is str:
        s = s.encode()
    return s


def ensure_str(s):
    if type(s) is bytes:
        s = s.decode()
    return s


def mapped(headers):
    """S3到COS参数的一个映射"""
    _headers = dict()
    for i in headers:
        if i in map_list:
            if i == 'Metadata':
                for meta in headers[i]:
                    _headers[meta] = headers[i][meta]
            else:
                _headers[map_list[i]] = headers[i]
        else:
            raise CosClientError('No Parameter Named ' + i + ' Please Check It')
    return _headers


async def check_object_content_length(data):
    """put_object接口和upload_part接口的文件大小不允许超过5G"""

    content_length = 0
    if isinstance(data, (str, bytes)):
        content_length = len(ensure_bytes(data))
    elif hasattr(data, 'fileno') and hasattr(data, 'tell'):
        fileno = data.fileno()
        total_length = os.fstat(fileno).st_size
        current_position = data.tell()
        if isawaitable(current_position):
            current_position = await current_position
        content_length = total_length - current_position
    if content_length > SINGLE_UPLOAD_LENGTH:
        raise CosClientError('The object size you upload can not be larger than 5GB in put_object or upload_part')


def get_md5(body):
    data = ensure_bytes(body)
    return md5(data).hexdigest()


async def get_content_md5(body):
    if isinstance(body, (str, bytes)):
        return get_md5(body)
    elif hasattr(body, 'tell') and hasattr(body, 'seek') and hasattr(body, 'read'):
        file_position = body.tell()  # 记录文件当前位置
        if isawaitable(file_position):
            file_position = await file_position
        data = body.read()
        if isawaitable(data):
            data = await data
        md5_str = get_md5(data)
        seek = body.seek(file_position)  # 恢复初始的文件位置
        if isawaitable(seek):
            await seek
        return md5_str


def dict2xml(d, root=b'Root', rules=None):
    if rules is None:
        rules = {}
    root = ensure_bytes(root)
    xml = [b'<%s>' % root]
    for el in d:
        if el in rules:
            xml.append(rules[el](d[el]))
        elif type(d[el]) is dict:
            xml.append(dict2xml(d[el], root=el))
        elif isinstance(d[el], (tuple, list)):
            xml += [dict2xml(x, el) for x in d[el]]
        elif isinstance(d[el], (str, bytes)):
            xml.append(b'<%s>%s</%s>' % (ensure_bytes(el), ensure_bytes(d[el]), ensure_bytes(el)))

    xml.append(b'</%s>' % root)
    return b''.join(xml)


def xml2dict(xml, lst=None):
    if lst is None:
        lst = []
    xml = ensure_str(xml).strip()
    root = re.compile(r'<(\w+)>([\s\S]+?)</\1>', re.M).findall(xml)
    if not root:
        return xml
    ret = {}
    lst_dict = defaultdict(list)
    for k, v in root:
        if k in lst:
            lst_dict[k].append(xml2dict(v, lst))
        else:
            ret[k] = xml2dict(v, lst)
    ret.update(lst_dict)
    return ret


def format_path(path):
    """检查path是否合法,格式化path"""
    if not isinstance(path, (str, bytes)):
        raise CosClientError("key is not string")
    if not path:
        raise CosClientError("Key is required not empty")
    path = ensure_str(path)
    if path[0] == u'/':
        path = path[1:]
    # 提前对path进行encode
    path = quote(ensure_bytes(path), b'/-_.~')
    return path
