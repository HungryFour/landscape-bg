from flask import Response

from controllers.base_controllers import BaseController


class ImageController(BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, file_name):
        with open(r'./resumes/{}'.format(file_name), 'rb') as f:
            image = f.read()
            resp = Response(image, mimetype="image/jpg")
            return resp
