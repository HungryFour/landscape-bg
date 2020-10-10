from flask import request
from flask_restful import Resource
from errors.error_handler import InvalidUsageException
from services.token_service import TokenService
from tools.utils import dict_strip


class BaseController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_argument_dict(self, must_keys=None, check_token=True):
        """
        :param must_keys: must_keys=["aa", "bb"] 判断出入列表里的值,是否在请求参数里,没有报错
        :return:
        """
        # 获取参数字典
        request_args = self.get_request_content()
        print("request_args解析后:\n", request_args)

        # 验证用户
        if check_token:
            access_token = request.headers.get('AccessToken')
            user_id = request_args.get("user_id")
            if not access_token:
                print("AccessToken 缺失")
                self.return_error(20003)
            if not user_id:
                print("UserID 缺失")
                self.return_error(20003)

            check_result = TokenService().check_access_token(request_args.get("user_id"), access_token)
            if not check_result:
                self.return_error(20019)

        # 判断必填字段
        if must_keys:
            for key in must_keys:
                if key not in request_args:
                    print("请求缺少 [%s] 参数" % key)
                    self.return_error(20003)
        return request_args

    def get_request_content(self):
        """
        获取请求参数,如果参数中有data字段,直接返回data字段内容
        :return:
        """
        try:
            request_type = request.headers.get('Content-Type')
            print("request.get_json()：", request.get_json())
            if request_type:
                content_type = request_type.split(';')[0].lower()
                if content_type == "application/json":
                    args = request.get_json()
                elif request_type == "application/x-www-form-urlencoded":
                    args = request.args
                else:  # multipart/form-data
                    args = request.form
                # args = args.to_dict()
            else:
                args = {}
                for i in request.values:
                    for k, v in i.items():
                        args[k] = v
            request_args = dict_strip(args)
            return request_args
        except Exception as error:
            print(str(error))
            self.return_error(10006, error_msg="解析参数出现错误,请重新尝试")

    def return_error(self, error_code, error_msg=None, status_code=400):
        raise InvalidUsageException(error_code, error_msg, status_code)
