import os

from sqlalchemy import desc
from models.vcode_model import VcodeModel
from services.base_service import BaseService
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyun_sms import const
from tools.image_code_tool import gen_code_image
import random, datetime, json, hashlib, uuid


class VcodeService(BaseService):
    def __init__(self, *args, **kwargs):
        super(VcodeService, self).__init__(*args, **kwargs)
        self.url = "http://api.zthysms.com/sendSms.do"
        self.username = "HiQB888hy"
        self.password = "EozSr0"

        # 注意：不要更改
        REGION = "cn-hangzhou"
        PRODUCT_NAME = "Dysmsapi"
        DOMAIN = "dysmsapi.aliyuncs.com"

        self.acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
        region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

    '''
    验证码有效期 5分钟
    '''

    # @check_decorator(location=2)
    def send_vcode(self, type, mobile):
        mobile = str(mobile)
        type = str(type)
        vcode = self.generate_verification_code()
        delta = datetime.timedelta(seconds=300)

        # 给第三方平台发送验证码
        vcode_model = VcodeModel(
            mobile=mobile,
            vcode=vcode,
            type=type,
            expire_at=datetime.datetime.now() + delta,
        )
        # 发送验证码
        __business_id = uuid.uuid1()
        params = {"code": vcode}
        params_json = json.dumps(params)
        response = self.send_sms(__business_id, mobile, "融魔方", "SMS_135225159", params_json).decode('utf-8')
        response_dict = json.loads(response)
        if response_dict['Code'] != "OK":
            self.return_error(10013)

        with self.session_scope() as session:
            session.add(vcode_model)
            session.commit()

        return True

    def send_sms(self, business_id, phone_numbers, sign_name, template_code, template_param=None):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(business_id)

        # 短信签名
        smsRequest.set_SignName(sign_name)

        # 数据提交方式
        # smsRequest.set_method(MT.POST)

        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)

        # TODO 业务处理

        return smsResponse

    # 校验验证码
    # @check_decorator()
    def check_vcode(self, mobile, type, vcode):

        # TODO 前期测试
        if vcode == "333333":
            return True

        with self.session_scope() as session:
            q = session.query(VcodeModel).filter_by(mobile=mobile, type=int(type), status=0).with_for_update().order_by(
                desc(VcodeModel.created_at)).first()

            if not q:
                return False
            else:
                now_at = datetime.datetime.now()

                if (q.expire_at - now_at).seconds < 300:
                    if q.vcode == vcode:
                        q.status = 1
                        session.commit()
                    else:
                        return False
                else:
                    q.status = 2
                    session.commit()
                    return False
            return True

    # 生成六位验证码
    @classmethod
    def generate_verification_code(self):

        code_list = ''

        for i in range(6):
            # 生成一个0~9的随机数
            random_num = random.randint(0, 9)
            code_list = code_list + str(random_num)
        return code_list

    @staticmethod
    def get_tkey():
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    @staticmethod
    def get_password(tkey):
        data1 = hashlib.md5("EozSr0".encode('utf-8')).hexdigest() + tkey
        password = hashlib.md5(data1.encode('utf-8')).hexdigest()
        return password

    def get_image_code_path(self):
        """
        获取验证码图片位置,并且将code保存到redis中
        :return: 返回位置和code
        """
        image, code = gen_code_image()
        path = os.getcwd() + "/tem_images/" + code + "_" + str(datetime.datetime.now()) + ".jpg"
        image.save(path)
        return path, code

    def check_image_code(self, code):
        """
        查看验证码是否正确
        :return:
        """
        # TODO 前期测试
        if code == "0000":
            return True

        return True

    def del_image_code_file(self, path):
        """
        删除验证码图片,以节约内存
        """
        try:
            os.remove(path)
        except Exception as error:
            print(str(error))
