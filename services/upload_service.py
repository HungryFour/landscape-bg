from services.base_service import BaseService
from tools.file_tool import save_file_to_the_local


class UploadService(BaseService):
    def __init__(self, *args, **kwargs):
        super(UploadService, self).__init__(*args, **kwargs)

    def upload_file(self, file, file_name=None):

        resume_path, resume_name, resume_type = "", "", ""
        try:
            resume_path, resume_name, resume_type = save_file_to_the_local(file, file_name)
        except Exception as error:
            print(str(error))
            self.return_error(20010)

        return {
            "resume_path": resume_path,
            "resume_name": resume_name,
        }
