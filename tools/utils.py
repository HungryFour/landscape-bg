import datetime
import decimal
import socket
import requests
import json
from dateutil.relativedelta import *
import config


def detect_file(find_file_name, dir_path=None):
    """
    在项目目录下,递归查找文件,找到返回一个字典{"root":"/test", "file":"/test/t.py"},未找到返回FALSE
    :param dir_path: 默认为空时在项目主目录下查找,否则在dir_path目录下查找,dir_path必须是系统真实路径,不能是相对路径
    :param find_file_name: 要查找的文件名,需要带后缀
    :return:
    """
    import os
    if not dir_path:
        server_name = config.get_bases_conf().get('server_name')
        real_path = os.path.realpath(__file__)
        file_index = real_path.rfind(server_name)
        dir_path = os.path.abspath(os.path.join(real_path[:file_index], server_name))
    for root, dirs, files in os.walk(dir_path):
        if find_file_name in files:
            return dict(root=root, file=os.path.abspath(os.path.join(root, find_file_name)))

    return False


def detect_python_path(find_file_name):
    """
    检测文件是否在Python环境变量里,如果存在返回这个文件的真实完整路径,否则加载到系统环境变量里
    :param find_file_name: 文件名 "logging.json"
    :return:
    """
    import os
    import sys
    for iter_path in sys.path:
        iter_root, iter_file = os.path.split(iter_path)
        if find_file_name == iter_file:
            return iter_path

    res = detect_file(find_file_name)
    if not res:
        raise Exception("File does not exist")
    real_name = res["file"]
    sys.path.append(real_name)
    return real_name


def get_decimal(data, digits=4, decimal_type="down"):
    if decimal_type.lower() == "up":
        round_type = decimal.ROUND_UP
    elif decimal_type.lower() == "round":
        round_type = decimal.ROUND_HALF_EVEN
    else:
        round_type = decimal.ROUND_DOWN

    if not data:
        data = "0"

    if not isinstance(data, str):
        data = str(data)

    decimal_template = "0." + "0" * digits
    return decimal.Decimal(data).quantize(decimal.Decimal(decimal_template), round_type)


def decimal_two_up(n):
    # 保留两位小数向上取
    return get_decimal(n, 2, "up")


def decimal_two_down(n):
    # 保留两位小数向下取
    return get_decimal(n, 2, "down")


def decimal_two(n):
    # 保留两位小数四舍五入
    return get_decimal(n, 2, "round")


def months_diff(day1, day2):
    # 获取两个日期的月份差绝对值
    n = (day2.year - day1.year) * 12 - day1.month + day2.month
    return abs(n)


def get_project_periods(full_mark_at, final_payback_at):
    # 获取项目的期数
    month = months_diff(full_mark_at, final_payback_at)
    if final_payback_at.day >= full_mark_at.day:
        month += 1
    return month


def get_project_payback_at_list(full_mark_at, final_payback_at, is_repayment=True):
    '''
    获取项目还款日期列表
    :param full_mark_at: 满额日期
    :param final_payback_at: 最终还款日期
    :param is_repayment: 是否是还款日计算 如果是还款日,日期-1天 回款日不减
    :return:
    '''
    days = 1 if is_repayment else 0
    # 1.0获取项目期数
    periods = get_project_periods(full_mark_at, final_payback_at)
    payback_at_list = []
    # 2.0计算所有还款日期
    for period in range(1, periods):
        payback_at_list.append(full_mark_at + relativedelta(months=+period) - datetime.timedelta(days=days))
    payback_at_list.append(final_payback_at)
    return payback_at_list


def days_diff(day1, day2):
    '''
    :param day1:
    :param day2:
    :return:
    '''
    if isinstance(day1, datetime.datetime):
        day1 = datetime.date(day1.year, day1.month, day1.day)
    if isinstance(day2, datetime.datetime):
        day2 = datetime.date(day2.year, day2.month, day2.day)
    # 获取两个日期之间的天数差
    a = (day2 - day1).days
    return abs(a)


def n_day_ago(date=None, n=0):
    if not date:
        date = datetime.date.today()
    day = date - datetime.timedelta(days=n)
    return day


def dict_strip(data):
    args = {}
    for k, v in data.items():
        # 如果v值存在,并且V值不等于空字符串,则将参数加到request_args中
        if v and str(v).strip():
            args[k] = v

    return args


def diy_dict_format(data, func=None):
    """
    字典格式化,按照传入相应方法进行转化
    :param data:
    :param func:
    :return:
    """
    if not func:
        func = decimal_two_down
    if isinstance(data, dict):
        tmp_dict = {}
        for k, v in data.items():
            if isinstance(v, float):
                tmp_val = func(v)
            elif isinstance(v, (dict, list)):
                tmp_val = diy_dict_format(v)
            else:
                tmp_val = v
            tmp_dict[k] = tmp_val
        return tmp_dict
    elif isinstance(data, list):
        tmp_list = []
        for item in data:
            tmp_item = diy_dict_format(item)
            tmp_list.append(tmp_item)
        return tmp_list
    else:
        return data


def float_2_str_save_precision(data, precision=2):
    """
    float类型 转化 字符串,保留参数要求的小数点精度
    :param data: float 类型
    :param precision: 精度单位 默认保留小数点 2位
    :return:
    """
    fmt = "%." + str(precision) + "f"
    if isinstance(data, float):
        return fmt % data
    return str(data)


def get_local_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


# 获取外网IP
def get_out_host_ip():
    url = r'http://jsonip.com'
    key = '"ip":'
    r = requests.get(url)
    txt = r.text
    key_index = txt.find(key)
    ip = "0.0.0.0" if key_index < 0 else txt[key_index + len(key):].split('"')[1]
    return ip


# 本地存取常量
def get_config_local(key="out_host_ip"):
    """
    读取本地config_local.json文件,根据key取相应的值
    :param key:
    :return:
    """
    config_local_path = detect_file("config_local.json")
    val = None
    if not config_local_path:
        utils_path = detect_file("utils.py")
        if not utils_path:
            return
        config_local_path = utils_path["root"] + "/" + "config_local.json"
        with open(config_local_path, "w+") as f:
            out_host_ip = get_out_host_ip()
            data = {"out_host_ip": out_host_ip}
            f.write(json.dumps(data))
    else:
        with open(config_local_path["file"], "r") as f:
            data = json.load(f)
            out_host_ip = data["out_host_ip"]
            if key in data:
                val = data[key]

    return out_host_ip if key == "out_host_ip" else val


def formate_args(args, format_str=False, format_keys=True,
                 format_eval=True):
    """
    参数格式化
    :param args: 参数字典
    :param format_str: 是否需要把所有int类型,强转成字符串
    :param format_eval: 是否开启 把字符串 '["a","b"]' '{"a":1,"b":"1"}' 强转回list dict
    :param format_keys: 是否开启 把key的值 转为全小写
    :return:
    """
    tmp = {}
    for key, value in args.items():
        if format_eval and isinstance(value, str) and value:
            if value[0] in ("[", "{", "(") and value[-1] in ("]", "}", ")"):
                value = eval(value)
        if format_keys:
            key_lower = key.lower()
        else:
            key_lower = key
        if format_str:
            if isinstance(value, (int, float)):
                value = str(value)
        tmp[key_lower] = value
    formated_args = dict(filter(lambda x: x[1] != '', tmp.items()))
    return formated_args


def str_to_int(str=None, replace=None):
    """
    字符串转数字
    :param str: 目标字符串
    :param replace: 如果不能转化,替换为
    :return:
    """
    try:
        if str.isdigit():
            return int(str)
        else:
            return replace
    except Exception:
        return replace


JOB_STATUS_DIC = {"在职": 1, "离职": 2, "看机会": 3}
EDUCATION_DIC = {"未知": 0, "专科": 1, "本科": 2, "研究生": 3, "博士": 4}
