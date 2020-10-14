from flask import Response
import mimetypes
from controllers.base_controllers import BaseController


class FileController(BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, file_name):
        with open(r'./resumes/{}'.format(file_name), 'rb') as f:
            f = f.read()
            resp = Response(f, mimetype=mimetypes.guess_type(file_name)[0])
            return resp
