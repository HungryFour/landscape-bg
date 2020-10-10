import datetime
import time
import uuid
from models.api_token_model import ApiTokenModel
from services.base_service import BaseService
from tools.utils import n_day_ago


class TokenService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.AccessTokenExpireTime = 30 * 24 * 60 * 60

    def generator_user_tokens(self, user_id):
        """
        生成用的access_token和refresh_token
        :param user_id:
        :return:
        """
        with self.session_scope() as session:
            # 将之前的token删除
            self.delete_all_token(user_id)

            # 生成token
            access_token_expire_time = datetime.datetime.fromtimestamp(int(time.time()) + self.AccessTokenExpireTime)
            refresh_token_expire_time = datetime.datetime.fromtimestamp(int(time.time()) + 365 * 24 * 60 * 60)
            access_token = self.generate_token(user_id, uuid.uuid4().hex)
            refresh_token = self.generate_token(user_id, uuid.uuid4().hex)

            access_token_model = ApiTokenModel(user_id=user_id, token_type="AccessToken",
                                               token=access_token,
                                               expire_at=access_token_expire_time, deleted=False)
            refresh_token_model = ApiTokenModel(user_id=user_id, token_type="RefreshToken",
                                                token=refresh_token,
                                                expire_at=refresh_token_expire_time, deleted=False)
            session.add(access_token_model)
            session.add(refresh_token_model)
            session.commit()

            result = {
                "access_token": access_token,
                "access_token_expire_time": str(access_token_expire_time),
                "refresh_token": refresh_token,
                "refresh_token_expire_time": str(refresh_token_expire_time)
            }
            return result

    def refresh_user_access_token(self, user_id):
        """
        刷新用户access_token
        :param user_id: 用户ID
        :return:
        """
        with self.session_scope() as session:
            # 1.0 获取用户可用时间大约2天的token
            access_token = session.query(ApiTokenModel).filter(ApiTokenModel.deleted == False,
                                                               ApiTokenModel.expire_at > n_day_ago(datetime.datetime.now(), -2),
                                                               ApiTokenModel.token_type == "AccessToken",
                                                               ApiTokenModel.user_id == user_id).first()
            # 2.0 验证用户名下有没有可用的access_token,如果有,则返回
            if access_token:
                return {
                    "access_token": access_token.token,
                    "access_token_expire_time": str(access_token.expire_at)
                }
            # 3.0将之前的token删除
            self.delete_all_token(user_id)
            # 4.0生成token
            access_token_expire_time = datetime.datetime.fromtimestamp(int(time.time()) + self.AccessTokenExpireTime)
            access_token = self.generate_token(user_id, uuid.uuid4().hex)

            access_token_model = ApiTokenModel(user_id=user_id, token_type="AccessToken",
                                               token=access_token,
                                               expire_at=access_token_expire_time, deleted=False)
            session.add(access_token_model)
            session.commit()

            return {
                "access_token": access_token,
                "access_token_expire_time": str(access_token_expire_time)
            }

    def delete_all_token(self, user_id):
        """
        将用户所有的token都删除
        :param user_id:
        :return:
        """
        with self.session_scope() as session:
            # 将之前的token删除
            token_list = session.query(ApiTokenModel).filter_by(user_id=user_id,
                                                                deleted=False).with_for_update().all()
            for token in token_list:
                token.deleted = True
            session.commit()

    def delete_access_token(self, user_id):
        """
        将用户所有的access_token都删除
        :param user_id:
        :return:
        """
        with self.session_scope() as session:
            # 将之前的token删除
            token_list = session.query(ApiTokenModel).filter_by(user_id=user_id, token_type="AccessToken",
                                                                deleted=False).with_for_update().all()
            for token in token_list:
                token.deleted = True
            session.commit()

    def generate_token(self, user_id, uuid4):
        """
        token 生成规则 = user_id + timestamp (交错穿插) + uuid(随机数)
        :param user_id:
        :param uuid4:
        :return:
        """
        user_id = str(user_id)
        timestamp = str(int(time.time()))
        token = ""
        for index in range(len(user_id) + len(timestamp)):
            if index < len(user_id):
                token += user_id[index]

            if index < len(timestamp):
                token += timestamp[index]

        return token + uuid4

    def get_access_token(self, user_id):
        """
        内部方法,只能用于验证用户,不能返回
        通过user_id获取用户token,先查看redis中是否有.如果没有在进行数据库查询
        :param user_id: 用户ID
        :return:
        """
        # # 1.0 从redis中查取
        # access_token = RedisTools().get(user_id)
        # if access_token:
        #     return str(access_token, encoding='utf-8')
        # 2.0 从数据库中查取
        with self.session_scope() as session:

            token = session.query(ApiTokenModel.token).filter(ApiTokenModel.user_id == user_id, ApiTokenModel.token_type == "AccessToken",
                                                              ApiTokenModel.deleted == False,
                                                              ApiTokenModel.expire_at > datetime.datetime.now()).first()
            if not token:
                # 用户token过期
                self.return_error(20019)
            return token.token

    def check_access_token(self, user_id, token):
        """
        对比用户token是否一致
        :param user_id: 用户ID
        :param token: token
        :return:
        """
        access_token = self.get_access_token(user_id)
        return access_token == token

    def refresh_token(self, user_id, refresh_token):
        """
        刷新Token
        :param user_id: 用户ID
        :param refresh_token: refresh_token
        :return:
        """
        with self.session_scope() as session:
            refresh_token = session.query(ApiTokenModel).filter(ApiTokenModel.token == refresh_token, ApiTokenModel.deleted == False,
                                                                ApiTokenModel.expire_at > datetime.datetime.now(),
                                                                ApiTokenModel.token_type == "RefreshToken",
                                                                ApiTokenModel.user_id == user_id).first()
            #  如果refresh_token通过校验
            if refresh_token:
                return TokenService().refresh_user_access_token(user_id)
            else:
                self.return_error(20022)
