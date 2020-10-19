from flask import request

from controllers.base_controllers import BaseController
from services.upload_service import UploadService
from tools.file_tool import allowed_file


class UploadFileController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):

        print("request.files:", request.files)

        arg = self.get_argument_dict(check_token=False)

        file = request.files.get('file', None)

        if not file:
            self.return_error(20008)
        if not allowed_file(file.mimetype):
            self.return_error(20009)

        result = UploadService().upload_file(file, arg.get("name"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }
