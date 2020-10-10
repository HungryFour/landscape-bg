from flask import make_response, send_file
from controllers.base_controllers import BaseController
from services.vcode_service import VcodeService


class SendVCodeController(BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        """
        发送验证码
          :param user_mobile: 手机号码
          :param type : 验证码类型 0）注册 1）更改密码 2登录
        :return:
        """
        argument_dict = self.get_argument_dict(must_keys=['user_mobile', 'image_code', 'type'], check_token=False)
        user_mobile = str(argument_dict['user_mobile'])
        image_code = str(argument_dict['image_code'])
        send_type = str(argument_dict['type'])

        # # 1.0 判断用户注册状态
        # us = UserService()
        # result = us.is_register(user_mobile)
        # # 如果类型是注册,注册则报错
        # if send_type == "0":
        #     if result:
        #         self.return_error(20018)
        # elif send_type == "1" or send_type == "2":
        #     # 如果类型是更改密码和登录,则如果没有该用户报错
        #     if not result:
        #         self.return_error(20001)
        #
        # # 2.0 判断图片验证码是否正确
        # result = VcodeService().check_image_code(str(image_code))
        # if not result:
        #     self.return_error(20016, error_msg="图形验证码错误,请刷新后重试")
        # # 3.0 用户校验通过,发送验证码
        # service = VcodeService()
        # result = service.send_vcode(send_type, user_mobile)
        return {
            "status": {}
        }


class CheckVcodeController(BaseController):
    def __init__(self, *args, **kwargs):
        super(CheckVcodeController, self).__init__(*args, **kwargs)

    '''
    校验短信验证码
    :param user_mobile: 手机号码
    :param type : 验证码类型 0）注册 1）更改密码 2) 忘记密码
    :param vcode : 验证码
    '''

    def post(self):
        argument_dict = self.get_argument_dict(check_token=False)

        user_mobile = argument_dict['user_mobile']
        vcode = argument_dict['vcode']
        type = argument_dict['type']

        vcode_service = VcodeService()
        result = vcode_service.check_vcode(user_mobile, int(type), vcode)
        return {
            "status": result
        }


class GetImageCodeController(BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        """
        获取图片验证码
        :return:
        """
        arg = self.get_argument_dict(check_token=False)
        print(arg)
        path, code = VcodeService().get_image_code_path()
        try:
            response = make_response(send_file(path))
            response.headers["Content-Disposition"] = "attachment; filename=code.jpg;"
            return response
        finally:
            VcodeService().del_image_code_file(path)
            print(path)
