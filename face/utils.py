import json


# 封装基础返回数据
def res_success(data=""):
    result = {}
    result["message"] = "success"
    result["code"] = 1
    result["data"] = data
    return json.dumps(result, ensure_ascii=False)


# 封装基础返回数据
def res_fail(data=""):
    result = {}
    result["message"] = "fail"
    result["code"] = -1
    result["data"] = data
    return json.dumps(result, ensure_ascii=False)