from controllers.base_controllers import BaseController


class TestController(BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        return {"status": "请求成功"}
