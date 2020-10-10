import base64

from flask import jsonify
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized, Forbidden, MethodNotAllowed, \
    InternalServerError
from app import app

from errors.error_handler import InvalidUsageException


@app.errorhandler(BadRequest)
def bad_request(error):
    response = jsonify()
    response.headers["Error_Code"] = 400
    response.headers["Error_Desc"] = str(error)
    response.headers["Error_Msg"] = str(error)
    response.status_code = 400
    return response


@app.errorhandler(Unauthorized)
def unauthorized(error):
    response = jsonify()
    response.headers["Error_Code"] = 401
    response.headers["Error_Desc"] = str(error)
    response.headers["Error_Msg"] = str(error)
    response.status_code = 401
    return response


@app.errorhandler(Forbidden)
def forbidden(error):
    response = jsonify()
    response.headers["Error_Code"] = 403
    response.headers["Error_Desc"] = str(error)
    response.headers["Error_Msg"] = str(error)
    response.status_code = 403
    return response


@app.errorhandler(NotFound)
def not_found(error):
    response = jsonify()
    response.headers["Error_Code"] = 404
    response.headers["Error_Desc"] = str(error)
    response.headers["Error_Msg"] = str(error)
    response.status_code = 404
    return response


@app.errorhandler(MethodNotAllowed)
def method_not_allow(error):
    response = jsonify()
    response.headers["Error_Code"] = 405
    response.headers["Error_Desc"] = str(error)
    response.headers["Error_Msg"] = str(error)
    response.status_code = 405
    return response


@app.errorhandler(InternalServerError)
def server_error(error):
    response = jsonify()
    response.headers["Error_Code"] = 400
    response.headers["Error_Desc"] = str(error)
    response.headers["Error_Msg"] = str(error)
    response.status_code = 400
    return response


@app.errorhandler(InvalidUsageException)
def handle_invalid_usage(error):
    return {
        "code": error.error_code,
        "msg": error.error_msg,
        "data": {}
    }


@app.before_first_request
def before_first_request():
    print('The service is started and the request first starting!')


def err_init():
    # 该方法勿删
    pass
