from services.base_service import BaseService
from services.token_service import TokenService
from models.admin_user_model import AdminUserModel


class AdminUserService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_register(self, user_account):
        """
        查看Admin用户是否注册
        :param user_account: 用户手机号
        :return:
        """
        with self.session_scope() as session:
            q = session.query(AdminUserModel).filter(AdminUserModel.user_account == user_account, AdminUserModel.deleted == False,
                                                     AdminUserModel.status == 0).first()
            # 1.0 判断是否有该账户
            if q:
                return True
            else:
                return False

    def user_level(self, user_id):
        """
        查看Admin用户等级
        :param user_id: user_id
        :return:
        """
        with self.session_scope() as session:
            q = session.query(AdminUserModel).filter(AdminUserModel.user_id == user_id, AdminUserModel.deleted == False,
                                                     AdminUserModel.status == 0).first()
            # 1.0 判断是否有该账户
            if q:
                return q.level
            else:
                self.return_error(20001)

    def register(self, creator_id, user_account, user_mobile, user_name, level, password):
        """
        注册Admin用户
        :param creator_id: 创建者ID
        :param user_account: 用户账号
        :param user_mobile: 用户手机号
        :param user_name: 用户姓名
        :param level: 用户等级
        :param password: 用户密码
        :return:
        """
        # 1.0 查看创建者用户权限
        if self.user_level(creator_id) != 9:
            self.return_error(20028)

        # 2.0 查看该用户账号是否被使用
        if self.is_register(user_account):
            self.return_error(20018)

        # 3.0 创建用户
        with self.session_scope() as session:
            user = AdminUserModel(
                creator_id=creator_id,
                user_account=user_account,
                user_mobile=user_mobile,
                user_name=user_name,
                level=level,
                password=password
            )
            session.add(user)
            session.commit()
        return True

    def login(self, user_account, password):
        '''
        用户登录
        :param user_account: 用户账号
        :param password: 密码
        '''
        with self.session_scope() as session:
            user = session.query(AdminUserModel).filter(AdminUserModel.user_account == user_account, AdminUserModel.deleted == False,
                                                        AdminUserModel.status == 0).first()
            # 1.0 判断用户是否存在
            if not user:
                self.return_error(20001)
            # 2.0 判断用户密码是否正确
            if password != user.password:
                self.return_error(20015)
            # 3.0 生成TOKEN
            ts = TokenService()
            result = ts.generator_user_tokens(user.user_id)
            result.setdefault("user_id", user.user_id)
            result.setdefault("user_account", user.user_account)
            result.setdefault("user_mobile", user.user_mobile)
            result.setdefault("user_name", user.user_name)
            result.setdefault("level", user.level)

            return result

    def update_user_info(self, user_id, user_mobile=None, user_name=None, target_user_id=None, level=None):
        """
        更改Admin用户信息
        :param user_id: user_id
        :param user_mobile: user_mobile
        :param user_name: user_name
        :param target_user_id: target_user_id
        :return:
        """

        if target_user_id:
            # 1.0 查看创建者用户权限
            if self.user_level(user_id) != 9:
                self.return_error(20028)
            user_id = target_user_id

        with self.session_scope() as session:
            user = session.query(AdminUserModel).filter(AdminUserModel.user_id == user_id, AdminUserModel.deleted == False,
                                                        AdminUserModel.status == 0).first()
            # 1.0 判断是否有该账户
            if not user:
                self.return_error(20001)

            if user_name:
                user.user_name = user_name
            if user_mobile:
                user.user_mobile = user_mobile
            if level:
                user.level = level

            session.commit()

            return True

    def update_user_password(self, user_id, oldpassword, newpassword):
        """
        更改Admin用户密码
        :param user_id: user_id
        :param oldpassword: 旧密码
        :param newpassword: 新密码
        :return:
        """

        with self.session_scope() as session:
            user = session.query(AdminUserModel).filter(AdminUserModel.user_id == user_id, AdminUserModel.deleted == False,
                                                        AdminUserModel.status == 0).first()
            # 1.0 判断是否有该账户
            if not user:
                self.return_error(20001)

            if user.password != oldpassword:
                self.return_error(20020)
            user.password = newpassword
            session.commit()

            return True

    def root_update_user_password(self, user_id, target_user_id, newpassword):
        """
        root用户更改Admin用户密码
        :param user_id: user_id
        :param target_user_id: 目标用户
        :param newpassword: 新密码
        :return:
        """

        # 1.0 查看创建者用户权限
        if self.user_level(user_id) != 9:
            self.return_error(20028)

        with self.session_scope() as session:
            user = session.query(AdminUserModel).filter(AdminUserModel.user_id == target_user_id, AdminUserModel.deleted == False,
                                                        AdminUserModel.status == 0).first()
            # 1.0 判断是否有该账户
            if not user:
                self.return_error(20001)

            user.password = newpassword
            session.commit()

            return True

    def update_user_level(self, user_id, target_user_id, level):
        """
        更改Admin用户等级
        :param user_id: user_id
        :param target_user_id: 目标用户ID
        :param level: 等级
        :return:
        """
        # 1.0 查看创建者用户权限
        if self.user_level(user_id) != 9:
            self.return_error(20028)

        with self.session_scope() as session:
            user = session.query(AdminUserModel).filter(AdminUserModel.user_id == target_user_id, AdminUserModel.deleted == False,
                                                        AdminUserModel.status == 0).first()
            # 1.0 判断是否有该账户
            if not user:
                self.return_error(20001, "目标用户不存在,请直接创建")
            user.level = int(level)
            session.commit()

            return True

    def remove_user(self, user_id, target_user_id):
        """
        删除用户
        :param user_id: user_id
        :param target_user_id: 目标用户ID
        :return:
        """
        # 1.0 查看创建者用户权限
        if self.user_level(user_id) != 9:
            self.return_error(20028)
        # 2.0 用户不能删除自己
        if user_id == target_user_id:
            self.return_error(20029)

        with self.session_scope() as session:
            user = session.query(AdminUserModel).filter(AdminUserModel.user_id == target_user_id, AdminUserModel.deleted == False,
                                                        AdminUserModel.status == 0).first()
            # 1.0 判断是否有该账户
            if not user:
                self.return_error(20001, "目标用户不存在,请直接创建")
            user.status = 1
            session.commit()

            return True

    def admin_users(self, user_id, target_user_id=None, user_account=None, user_mobile=None, user_name=None, level=None, limit=0, offset=0):
        """
        获取管理员列表
        :param user_id: 用户ID
        :param target_user_id: 目标用户ID
        :param user_account: 目标用户账号
        :param user_mobile: 目标用户手机号
        :param user_name: 姓名
        :param level: 等级
        :return:
        """

        # 1.0 查看创建者用户权限
        if self.user_level(user_id) != 9:
            self.return_error(20028)

        with self.session_scope() as session:
            q = session.query(AdminUserModel).filter(AdminUserModel.deleted == False,
                                                     AdminUserModel.status == 0)

            if target_user_id:
                q = q.filter(AdminUserModel.user_id == target_user_id)

            if user_account:
                q = q.filter(AdminUserModel.user_account == user_account)

            if user_mobile:
                q = q.filter(AdminUserModel.user_mobile == user_mobile)

            if user_name:
                q = q.filter(AdminUserModel.user_name == user_name)

            if level:
                q = q.filter(AdminUserModel.level == level)

            model_list = q.limit(limit).offset(offset).all()

            user_list = []
            for model in model_list:
                user = {
                    "user_id": model.user_id,
                    "user_account": model.user_account,
                    "user_mobile": model.user_mobile,
                    "user_name": model.user_name,
                    "level": model.level
                }
                user_list.append(user)
            return user_list

    def admin_hrs(self, limit=0, offset=0):
        """
        获取Hr列表
        :return:
        """
        with self.session_scope() as session:
            q = session.query(UserModel).filter(UserModel.deleted == False,
                                                UserModel.status == 0)
            all_count = q.count()

            model_list = q.limit(limit).offset(offset).all()

            user_list = []
            for model in model_list:
                user = {
                    "user_id": model.user_id,
                    "user_mobile": model.user_mobile,
                    "nickname": model.nickname,
                    "level": model.level,
                    "is_bind_zfb": model.is_bind_zfb
                }
                user_list.append(user)
            return user_list, all_count
