from controllers.base_controllers import BaseController
from services.resource_service import ResourceService


class ResourceController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        self.get_argument_dict(must_keys=["user_id"])
        resource_list = ResourceService().resources()
        result_list = []
        for resource in resource_list:
            result = {
                "id": resource.id,
                "created_at": str(resource.created_at),
                "video": resource.video,
                "cover_pic": resource.cover_pic,
                "title": resource.title,
                "info": resource.info,
                "category": resource.category,
                "director": resource.director,
                "resource_type": resource.resource_type
            }
            result_list.append(result)
        return {
            "code": 0,
            "msg": "success",
            "data": result_list
        }


class CreateResourceController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id"])

        print("arg:", arg)

        result = ResourceService().create_resource(video=arg.get("video"),
                                                   cover_pic=arg.get("cover_pic"),
                                                   title=arg.get("title"),
                                                   info=arg.get("info"),
                                                   category=arg.get("category"),
                                                   director=arg.get("director"),
                                                   resource_type=arg.get("resource_type"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class UpdateResourceController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id"])
        result = ResourceService().update_resource(resource_id=arg.get("id"),
                                                   video=arg.get("video"),
                                                   cover_pic=arg.get("cover_pic"),
                                                   title=arg.get("title"),
                                                   info=arg.get("info"),
                                                   category=arg.get("category"),
                                                   director=arg.get("director"),
                                                   resource_type=arg.get("resource_type"))

        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class RemoveResourceController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["user_id", "id"])
        result = ResourceService().remove_resource(resource_id=arg.get("id"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }
