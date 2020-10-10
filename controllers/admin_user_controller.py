from controllers.base_controllers import BaseController
from services.admin_user_service import AdminUserService


class AdminRegisterController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id", "user_account", "bcypt_password", "level"],
                                     check_token=True)

        creator_id = arg.get("user_id")
        user_account = arg.get("user_account")
        bcypt_password = arg.get("bcypt_password")
        level = arg.get("level")
        user_mobile = arg.get("user_mobile")
        user_name = arg.get("user_name")
        aus = AdminUserService()
        result = aus.register(creator_id, user_account, user_mobile, user_name, level, bcypt_password)
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class UpdateAdminInfoController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id"])
        user_id = arg.get("user_id")
        user_mobile = arg.get("user_mobile", None)
        user_name = arg.get("user_name", None)
        level = arg.get("level", None)
        target_user_id = arg.get("target_user_id", None)
        us = AdminUserService()
        result = us.update_user_info(user_id, user_mobile, user_name, target_user_id, level)
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class UpdateAdminLevelController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id", "target_user_id", "level"])
        user_id = arg.get("user_id")
        target_user_id = arg.get("target_user_id")
        level = arg.get("level")
        us = AdminUserService()
        result = us.update_user_level(user_id, target_user_id, level)
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class RemoveAdminUserController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id", "target_user_id"])
        user_id = arg.get("user_id")
        target_user_id = arg.get("target_user_id")
        us = AdminUserService()
        result = us.remove_user(user_id, target_user_id)
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class AdminLoginController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["username", "password"], check_token=False)
        user_account = arg.get("username")
        password = arg.get("password")

        print("=====", arg)

        us = AdminUserService()
        result = us.login(user_account=user_account, password=password)
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class UpdateAdminPasswordController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id", "oldpassword", "newpassword"])
        user_id = arg.get("user_id")
        oldpassword = arg.get("oldpassword")
        newpassword = arg.get("newpassword")
        us = AdminUserService()
        result = us.update_user_password(user_id, oldpassword, newpassword)
        return {
            "status": result
        }


class AdminUsersController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id"])
        user_id = arg.get("user_id")
        user_account = arg.get("user_account", None)
        user_mobile = arg.get("user_mobile", None)
        user_name = arg.get("user_name", None)
        level = arg.get("level", None)
        target_user_id = arg.get("target_user_id", None)

        limit = int(arg.get("page_size", "10"))
        offset = limit * (int(arg.get("page", "1")) - 1)

        us = AdminUserService()
        result = us.admin_users(user_id=user_id, target_user_id=target_user_id, user_mobile=user_mobile, user_account=user_account,
                                user_name=user_name, level=level, limit=limit, offset=offset)
        return {
            "status": result
        }
