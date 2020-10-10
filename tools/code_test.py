#
# request_args = {"a": "A", "b": None}
#
# args = {}
# for k, v in request_args.items():
#     # 如果v值存在,并且V值不等于空字符串,则将参数加到request_args中
#     if v and str(v).strip():
#         args[k] = v
#
# print(args)

import json

# ArrExpericeneDetail = ["2016-03 ~ 至今 北京网融天下金融信息服务有限公司 / 技术部 iOS高级开发工程师 VUE Python IOS 理财范App开发维护,权益平台后台开发,hi钱包产品后台开发。",
#                        "2015-10 ~ 2016-03 华夏康家(北京)生态科技有限公司 iOS开发 创业, 技术入股。主要负责公司 iOS端开发, 参与产品讨论等。",
#                        "2014-09 ~ 2015-10 北京易好捷互联网科技有限公司 ios开发工程师 iOS客户端开发"]
#
# json_str = json.dumps(ArrExpericeneDetail)
import os


def get_json_from_file(file_path):
    with open(file_path, 'r') as f:
        print(f)
        content = json.load(f)
        f.close()
    return content
#
#
# json_data = get_json_from_file("resume_test.json")
#
# age = str(json_data.get("Sex", "123"))
# if age.strip():
#     age = int(age)
# else:
#     age = 456
# print(age)

# print(json_data["EducationInfo"])
#
# print(json_data.get("SchoolRankings"))


