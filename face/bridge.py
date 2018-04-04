
from flask import Flask
import json
from flask import request
import ctypes
from face.utils import res_success, res_fail

ll = ctypes.cdll.LoadLibrary
lib = ll("/home/yanglin/yl/c++/arcsoft-arcface/arcface/src/libface.so")

app = Flask(__name__)

app.debug = False


# middelware #
@app.before_request
def http_begin_log():
    app.logger.info("Start" + request.method + request.url)
    # if request.method != 'GET':
    #     pass
    #     #app.logger.info("Data" + request.data)


@app.before_request
def auth():
    if request.method != 'GET':
        if 'auth' in request.json:
            auth = request.json["auth"]
            if auth == "123":
                pass
            else:
                return res_fail("权限不足")
        else:
            return res_fail("权限不足")
    else:
        auth = request.args.get('auth')
        if auth == "123":
            pass
        else:
            return res_fail("权限不足")


# @app.after_request
# def http_end_log(self):
#     pass
#     #app.logger.info("END" + request.method + request.url)


# router
@app.route('/camera', methods=['PUT'])
def open_camera():
    camera_num = request.json["cameraNum"]
    if camera_num:
        return res_fail("摄像头编号不能为空")
    result = lib.openCamera(camera_num)
    if result == -1:
        return res_fail("打开失败")
    else:
        return res_success()


@app.route('/close/camera', methods=['PUT'])
def close_camera():
    if 'cameraNum' in request.json:
        camera_num = request.json["cameraNum"]
        result = lib.freeOneCamera(camera_num)
        if result == 0:
            return res_fail("关闭失败")
        else:
            return res_success()
    else:
        return res_fail("摄像头编号不能为空")


@app.route('/close/cameras', methods=['PUT'])
def close_cameras():
    lib.freeAllCamera()
    return res_success()


@app.route('/cameras', methods=['GET'])
def get_cameras_info():
    lib.getAllCameraInfo()
    return res_success()


@app.route('/check/feature', methods=['GET'])
def check_feature_info():
    path = request.args.get('image')
    if path:
        result = lib.checkFeature(path)
        if result == -1:
            return res_fail("获取失败")
        return res_success()
    return res_fail("获取失败")


@app.route('/models', methods=['POST'])
def add_face_model():
    if 'id' in request.json and 'imageId' in request.json and 'type' in request.json and 'isActived' in request.json:
        id = request.json['id']
        imageId = request.json['imageId']
        type = request.json['type']
        is_actived = request.json['isActived']
        result = lib.addModel(id, imageId, type, is_actived)
        if result == 1:
            return res_success()
        else:
            return res_fail()
    return res_fail("请输入正确的参数")