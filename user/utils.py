from django.http import HttpRequest
from django.utils import timezone
from . import security, models, userconfig
import hashlib
import random
import re


def check_name(value: str):
    if len(value) < 2 or len(value) > 32:
        return False
    else:
        for _c in value:
            if('A' <= _c <= 'Z') or ('a' <= _c <= 'z') or ('0' <= _c <= '_9') or _c == "_":
                pass
            else:
                return False
        return True


def check_nickname(value: str):
    if len(value) < 1 or len(value) > 32:
        return False
    else:
        return True


def check_email(value: str):
    pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
    if re.match(pattern, value) is not None:
        return True
    else:
        return False


def check_md5(value: str):
    if len(value) != 32:
        return False
    else:
        for _c in value:
            if('0' <= _c <= '9') or ('a' <= _c <= 'f'):
                pass
            else:
                return False
        return True


def check_device_type(value: str):
    return value in map(lambda x: x[1], models.UserActivity.device_type_choices)


def check_software(value: str):
    return value in userconfig.software


def get_hash(value: str):
    md5 = hashlib.md5()
    md5.update(value.encode('utf-8'))
    return md5.hexdigest()


def make_uid(name: str, time: float):
    a = str(int(time))
    b = get_hash(name)
    c = str(random.randint(10, 99))
    return a + b + c


def encrypt_token(uid: str, time: float, software: str, device_type: str):
    """
    生成一个登录的token
    :param uid: 用户的uid
    :param time: 登录时间
    :param software: 软件名称
    :param device_type: 设备名称
    :return: token加密后的字符串
    """
    token_raw = f'{uid}::{software}::{str(time)}::{device_type}'
    return security.default_aes.encrypt(token_raw)


def decrypt_token(token: str):
    """
    获取原有的登录信息
    :param token: 登录的token
    :return:
    """
    token_raw = security.default_aes.decrypt(token)
    args = token_raw.split('::')
    return {'uid': args[0], 'time': float(args[1]), 'software': args[2], 'device_type': args[3]}


def default_time():
    return timezone.datetime(1970, 1, 1, 0, 0, 0, 0)


def format_time(time: timezone.datetime):
    return time.astimezone().strftime('%Y-%m-%d %H:%M:%S')


def get_request_ip(request: HttpRequest):
    try:
        return request.META['HTTP_X_FORWARDED_FOR']
    except KeyError:
        return request.META['REMOTE_ADDR']

