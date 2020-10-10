from flask import Flask
from flask_restful import Api
from flask_cors import *

from controllers.test_controller import TestController
from controllers.upload_file_controller import UploadFileController
from controllers.vcode_controller import GetImageCodeController, SendVCodeController
from controllers.admin_user_controller import AdminLoginController, AdminRegisterController, RemoveAdminUserController, \
    UpdateAdminInfoController, UpdateAdminLevelController, UpdateAdminPasswordController, AdminUsersController
from controllers.employee_controller import EmployeeController, CreateEmployeeController, UploadEmployeeController, RemoveEmployeeController
from controllers.article_controller import ArticelController, CreateArticelController, UploadArticelController, RemoveArticelController
from controllers.resource_controller import ResourceController, CreateResourceController, UpdateResourceController, RemoveResourceController
from controllers.image_controller import ImageController

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*',
     expose_headers=['Origin', 'Accept', 'Content-Type', 'Content-Disposition', 'Access-Control-Allow-Origin'])

from errors import error

error.err_init()
app.template_folder = "templates"
api = Api(app)

api.add_resource(TestController, "/test")

api.add_resource(GetImageCodeController, "/imagecode")  # 获取图片验证码
api.add_resource(SendVCodeController, "/vcode")  # 获取验证码
api.add_resource(ImageController, "/image/<file_name>")  # 获取图片

# Admin-Api
api.add_resource(AdminLoginController, "/admin/login")  # 登录
api.add_resource(AdminRegisterController, "/admin/register")  # 注册
api.add_resource(UpdateAdminInfoController, "/admin/update-userinfo")  # 更改用户信息
api.add_resource(RemoveAdminUserController, "/admin/remove-user")  # 删除用户
api.add_resource(UpdateAdminLevelController, "/admin/update-level")  # 更改用户等级
api.add_resource(UpdateAdminPasswordController, "/admin/change-password")  # 修改登录密码
api.add_resource(AdminUsersController, "/admin/users")  # 获取管理员列表

api.add_resource(EmployeeController, "/admin/employees")  # 获取员工列表
api.add_resource(CreateEmployeeController, "/admin/create/employee")  # 创建员工
api.add_resource(UploadEmployeeController, "/admin/update/employee")  # 修改员工
api.add_resource(RemoveEmployeeController, "/admin/remove/employee")  # 删除员工

api.add_resource(ArticelController, "/admin/articles")  # 获取文章列表
api.add_resource(CreateArticelController, "/admin/create/article")  # 创建文章
api.add_resource(UploadArticelController, "/admin/update/article")  # 修改文章
api.add_resource(RemoveArticelController, "/admin/remove/article")  # 修改文章

api.add_resource(ResourceController, "/admin/resources")  # 获取资源
api.add_resource(CreateResourceController, "/admin/create/resource")  # 创建资源
api.add_resource(UpdateResourceController, "/admin/update/resource")  # 更新资源
api.add_resource(RemoveResourceController, "/admin/remove/resource")  # 删除资源

api.add_resource(UploadFileController, "/admin/upload_file")  # 上传文件
