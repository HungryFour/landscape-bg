from errors.error_handler import InvalidUsageException


class RequestTools(object):
    def __init__(self):
        super(RequestTools, self).__init__()

    def return_error(self, err_code, error_msg=None, status_code=400):
        raise InvalidUsageException(err_code, error_msg, status_code)
