# TODO  错误码解释 1000X 系统级错误代码  2000X 服务级错误代码


def get_error_desc(error_code):
    if error_code in error_dic.keys():
        return error_dic[error_code]["desc"]
    else:
        return "error_code does not exists"


def get_error_msg(error_code):
    if error_code in error_dic.keys():
        return error_dic[error_code]["msg"]
    else:
        return "error_code does not exists"


error_dic = {
    10000: {
        "desc": "Other desc",
        "msg": "其他错误"
    },
    10001: {
        "desc": "System desc",
        "msg": "系统错误"
    },
    10002: {
        "desc": "Service unavailable",
        "msg": "服务暂停"
    },
    10003: {
        "desc": "Param desc, see doc for more info",
        "msg": "参数错误，请参考API文档"
    },
    10004: {
        "desc": "Job expired",
        "msg": "任务超时"
    },
    10005: {
        "desc": "Encrypt desc",
        "msg": "加密错误"
    },
    10006: {
        "desc": "Decrypt desc",
        "msg": "解密错误"
    },
    10007: {
        "desc": "Generate encryption key desc",
        "msg": "生成key错误"
    },
    10008: {
        "desc": "Repetition Request",
        "msg": "重复请求"
    },
    10009: {
        "desc": "Login frequency exceeds limit.",
        "msg": "登录次数超限"
    },
    10010: {
        "desc": "Send password frequently",
        "msg": "一分钟之内只允许发送一个验证码"
    },
    10011: {
        "desc": "send code exceeds limit.",
        "msg": "一日之内只允许发送不超过五个验证码"
    },
    10012: {
        "desc": "get code failed",
        "msg": "获取验证码失败"
    },
    10013: {
        "desc": "send vcode failed",
        "msg": "发送验证码失败"
    },
    20001: {
        "desc": "User does not exists",
        "msg": "用户不存在"
    },
    20002: {
        "desc": "Talent does not exists",
        "msg": "不存在该资源"
    },
    20003: {
        "desc": "Param is desc, please try again",
        "msg": "参数错误,请重新尝试"
    },
    20004: {
        "desc": "Account does not exists",
        "msg": "账户不存在或者账户状态不对"
    },
    20005: {
        "desc": "Talent had been recommend",
        "msg": "人才已经被推荐"
    },
    20006: {
        "desc": "Recommend does not exists",
        "msg": "没有这个职位"
    },
    20007: {
        "desc": "The user has not binded the Zhifubao",
        "msg": "用户未绑定支付宝"
    },
    20008: {
        "desc": "file is empty",
        "msg": "上传文件为空"
    },
    20009: {
        "desc": "The file format is not correct",
        "msg": "文件格式不正确"
    },
    20010: {
        "desc": "The file save error",
        "msg": "文件保存失败"
    },
    20011: {

        "desc": "The user had open the account or did not register",
        "msg": "用户已经开户或者还没有注册"
    },
    20012: {
        "desc": "The mobile format is desc",
        "msg": "手机号码格式不正确"
    },
    20014: {
        "desc": "Refresh Token Error",
        "msg": "登录凭证已过期,为了您的账户安全请重新登录"
    },
    20015: {
        "desc": "login password is desc",
        "msg": "登录密码错误"
    },
    20016: {
        "desc": "The mobile code verify failed",
        "msg": "验证码校验失败"
    },
    20017: {
        "desc": "The mobile code is expire",
        "msg": "验证码已经过期"
    },
    20018: {
        "desc": "The user had registed",
        "msg": "该用户已注册"
    },
    20019: {
        "desc": "Access Token Error",
        "msg": "AccessToken已经过期"
    },
    20020: {
        "desc": "The old password verify failed",
        "msg": "原密码错误，请重新输入"
    },
    20021: {
        "desc": "Decrypt Data Error",
        "msg": "登录凭证已过期,为了您的账户安全请重新登录"
    },
    20022: {
        "desc": "Refresh Token Error",
        "msg": "登录凭证已过期,为了您的账户安全请重新登录"
    },
    20023: {
        "desc": "Request Signature Error",
        "msg": "Signature 校验失败,请重新生成"
    },
    20024: {
        "desc": "Request Timestamp Error",
        "msg": "请求发送时间过长"
    },
    20025: {
        "desc": "Request Replay",
        "msg": "重复请求"
    },
    20026: {
        "desc": "User had nickname",
        "msg": "该用户已经有昵称"
    },
    20027: {
        "desc": "Nickname had repetition",
        "msg": "昵称重复了"
    },
    20028: {
        "desc": "Limited Authority",
        "msg": "权限不够"
    },
    20029: {
        "desc": "User can't remove self",
        "msg": "用户不能删除自己"
    },
    20030: {
        "desc": "Order does not exists",
        "msg": "订单不存在"
    },
    20031: {
        "desc": "Resume Error",
        "msg": "简历读取失败,请重新尝试"
    },
    30001: {
        "desc": "User balance is insufficient",
        "msg": "用户余额不足"
    },
    30002: {
        "desc": "User frozon amount is insufficient",
        "msg": "用户冻结金额不足"
    }
}
