from functools import wraps
from tools.request_tools import RequestTools
import re
from flask import request
from errors.error_handler import InvalidUsageException
from tools.redis_tool import RedisTools
import time
import random
import string
import hashlib


# def prevent_request_replay_decorator(func):
#     """
#     防重放
#     :param func:
#     :return:
#     """
#
#     def wrapped_func(*args, **kwargs):
#         verify_timeliness = False
#         if 'verify_timeliness' in kwargs:
#             verify_timeliness = kwargs['verify_timeliness']
#         if verify_timeliness:
#             request_header = request.headers
#             # 1.0 判断时间是否在请求限制时间内
#             timestamp = request_header.get("Timestamp", '0')
#             df_timestamp = int(time.time()) - int(timestamp)
#             if df_timestamp > 60 or df_timestamp < 0:
#                 return_error(error_code=20025)
#             # 2.0 检查signature是否在redis中,防止重复请求
#             c_signature = request_header.get("Signature")
#             redisTools = RedisTools()
#             if redisTools.exists(c_signature):
#                 return_error(error_code=20025)
#             # 将c_signature存到redis中
#             redisTools.set(name=c_signature, value="c_signature", ex=60)
#             # 3.0 验证c_signature合理性
#             nonce = request_header.get("Nonce", '')
#             source = request_header.get("Source", '')
#             s_signature = sha256_hex(str(timestamp) + str(nonce) + str(source))
#             if s_signature != c_signature:
#                 return_error(error_code=20023)
#         return func(*args, **kwargs)
#
#     return wrapped_func


def user_request_sameurl_in_limit_timeliness(error_code):
    def get_func(func):
        def wrapped_func(*args, **kwargs):
            request_header = request.headers
            # 获取用户手机号
            user_mibile = request_header.get("User-Mobile")
            # 获取请求地址
            path = request.path
            # 查看redis中有没有该请求
            redis_key = str(user_mibile) + str(path)
            redisTools = RedisTools()
            if redisTools.exists(redis_key):
                return_error(error_code=error_code)
            redisTools.set(name=redis_key, value=str(path), ex=60)
            return func(*args, **kwargs)

        return wrapped_func

    return get_func


def return_error(error_code, error_msg=None, status_code=400):
    raise InvalidUsageException(error_code, error_msg, status_code)


access_token_key = '123QW2'


def get_access_token(expire_time=60):
    hl = hashlib.md5()
    ran_str = str(''.join(random.sample(string.ascii_letters + string.digits, 8)))
    time_str = str(time.time())
    hl.update((time_str + ran_str + access_token_key).encode(encoding='utf-8'))
    access_token = hl.hexdigest()
    redis_tool = RedisTools()
    redis_tool.set(access_token, 1, ex=expire_time)
    return access_token


def check_access_token(access_token):
    if not access_token or not isinstance(access_token, str):
        return False
    redis_tool = RedisTools()
    get_result = redis_tool.get(access_token)
    if get_result:
        redis_tool.delete(access_token)
        return True
    return False


def get_access_token_by_condition(user_id, param1='', param2='', expire_time=60):
    hl = hashlib.md5()
    ran_str = str(''.join(random.sample(string.ascii_letters + string.digits, 8)))
    time_str = str(time.time())
    hl.update((time_str + ran_str + access_token_key).encode(encoding='utf-8'))
    access_token = hl.hexdigest()
    redis_tool = RedisTools()
    redis_key = str(user_id) + '_access_token'
    if param1:
        redis_key += '_' + str(param1)
    if param2:
        redis_key += '_' + str(param2)
    redis_tool.set(redis_key, access_token, ex=expire_time)
    return access_token


def check_access_token_by_condition(access_token, user_id, param1='', param2=''):
    if not access_token or not isinstance(access_token, str) or not user_id:
        return False
    redis_tool = RedisTools()
    redis_key = str(user_id) + '_access_token'
    if param1:
        redis_key += '_' + str(param1)
    if param2:
        redis_key += '_' + str(param2)
    print(redis_key)
    get_result = redis_tool.get(redis_key)
    print(get_result, access_token, get_result != access_token)
    if not get_result:
        return False
    get_result = str(get_result, encoding='utf-8')
    if get_result != access_token:
        return False
    redis_tool.delete(redis_key)
    return True


def check_decorator(check_type="mobile", location=1):
    """
    校验装饰器：

    :param check_type: 校验类型 默认为mobile - 手机号校验
    :param location: 校验参数位置

    1.要求调用service传参方式为*args的形式
    2.检验手机号码方法为@check(check_type="mobile", location=1)
    3.现在只支持手机号码校验，以后可以增加校验方式

    举个栗子：
    @check_decorator(check_type="mobile", location=0)
    def test(user_mobile):
        print(user_mobile)

    test("18611440468")

    print 18611440468
    """
    def check_method(func):
        @wraps(func)
        def check_args(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            if location > len(args) - 1:

                print(str(location) + " beyong args length ")
            else:
                if check_type == "mobile":
                    user_mobile = args[location]
                    regexp = r"^(1)\d{10}$"
                    # 开始验证
                    if re.match(regexp, user_mobile):
                        return func(*args, **kwargs)
                    else:
                        RequestTools().return_error(20012)
                        # InvalidUsageException(20037, "手机号码格式不正确", 400)
        return check_args

    return check_method
