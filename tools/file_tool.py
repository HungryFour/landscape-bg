import json
import os

# 设置允许上传的文件类型
import uuid

ALLOWED_MIMETYPE_DIC = {'image/jpeg': '.jpeg', 'application/pdf': '.pdf', "image/png": '.png', "image/jpg": '.jpg', "image/gif": '.gif'}


def save_file_to_the_local(file):
    """
    将文件保存到本地
    :param file: 文件
    :param name: 文件名称
    :return: path: 文件地址 name 文件名称
    """
    # root = os.getcwd()
    name = uuid.uuid4().hex + ALLOWED_MIMETYPE_DIC.get(file.mimetype)
    path = os.path.join("resumes/" + name)
    file.save(path)
    return path, name, ALLOWED_MIMETYPE_DIC.get(file.mimetype)


def allowed_file(mimetype):
    """
    检查文件类型是否合法
    :param mimetype: 原始文件mimetype
    :return:
    """
    # 判断文件的原始文件mimetype是否在配置项ALLOWED_MIMETYPE
    return mimetype in ALLOWED_MIMETYPE_DIC.keys()


def get_json_from_file(file_path):
    content = None
    try:
        with open(file_path, 'r') as f:
            print(f)
            content = json.load(f)
            f.close()
    except Exception as error:
        print(str(error))
    return content
