import requests
import base64
import json

URL = 'http://jljxjk.market.alicloudapi.com/aliyunapp/aliyunservice.aspx'
AppKey = "25130430"
AppSecret = "9562c076c1285f7d687001d4bcd5600d"
AppCode = "d83ab1d396a94b00a94c1ae382394f95"


def resume_parsing(file_path, file_type):
    # file_path = '/Users/wujianming/ZQ_Backend/resumes/简历demo2(原始简历).pdf'
    try:
        content = resume_base64(file_path)

        post_data = "cid=1&content=%s&ext=%s" % (content, file_type)

        headers = {"Authorization": "APPCODE " + AppCode, "Content-Type": "application/json; charset=UTF-8"}

        res = requests.post(URL, post_data, headers=headers)

        if res.status_code == 200:
            print(res.text)
            return json.loads(res.text)
        else:
            return None
    except Exception as error:
        print(str(error))
        return None


def resume_base64(file_path):
    with open(file_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode()  # 读取文件内容，转换为base64编码
        f.close()
    return content

# print(resume_parsing("12313123"))
