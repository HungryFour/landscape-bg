from controllers.base_controllers import BaseController
from services.employee_service import EmployeeService


class UserGetEmployeeController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        employees_list = EmployeeService().employees()

        result_list = []
        for employee in employees_list:
            result = {
                "id": employee.id,
                "created_at": str(employee.created_at),
                "name": employee.name,
                "avatar": employee.avatar,
                "title1": employee.title1,
                "title2": employee.title2,
                "production": employee.production,
            }
            result_list.append(result)

        return {
            "code": 0,
            "msg": "success",
            "data": result_list
        }


class EmployeeController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        self.get_argument_dict(must_keys=["user_id"])
        employees_list = EmployeeService().employees()

        result_list = []
        for employee in employees_list:
            result = {
                "id": employee.id,
                "created_at": str(employee.created_at),
                "name": employee.name,
                "avatar": employee.avatar,
                "title1": employee.title1,
                "title2": employee.title2,
                "production": employee.production,
            }
            result_list.append(result)

        return {
            "code": 0,
            "msg": "success",
            "data": result_list
        }


class CreateEmployeeController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id", "name", "avatar", "title1", "title2", "production"])

        result = EmployeeService().create_employee(creator_id=arg["user_id"],
                                                   name=arg.get("name"),
                                                   avatar=arg.get("avatar"),
                                                   title1=arg.get("title1"),
                                                   title2=arg.get("title2"),
                                                   production=arg.get("production"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class UploadEmployeeController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["id", "name", "avatar", "title1", "title2", "production"])

        result = EmployeeService().update_employee(employee_id=arg.get("id"),
                                                   name=arg.get("name"),
                                                   avatar=arg.get("avatar"),
                                                   title1=arg.get("title1"),
                                                   title2=arg.get("title2"),
                                                   production=arg.get("production"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class RemoveEmployeeController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["id"])
        result = EmployeeService().remove_employee(employee_id=arg.get("id"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }
