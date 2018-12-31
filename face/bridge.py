# encoding: utf-8
from flask import Flask
import json
from flask import request
import ctypes
from ctypes import cdll,byref,c_float
from face.utils import res_success, res_fail

# ll = ctypes.cdll.LoadLibrary
# lib = ll("/home/yanglin/yl/c++/arcsoft-arcface/arcface/src/libface.so")

app = Flask(__name__)

app.debug = False


# middelware #
@app.before_request
def auth():
    auth = request.headers.get('Authorization')
    if auth == "123":
        pass
    else:
        return res_fail("权限不足")


# router
@app.route('/camera', methods=['PUT'])
def open_camera():
    if 'cameraNum' not in request.json:
        return res_fail("摄像头编号不能为空")
    camera_num = request.json["cameraNum"]
    result = lib.openCamera(int(camera_num))
    if result == -1:
        return res_fail("开启失败")
    else:
        return res_success()


@app.route('/close/camera', methods=['PUT'])
def close_camera():
    if 'cameraNum' in request.json:
        camera_num = request.json["cameraNum"]
        result = lib.freeOneCamera(int(camera_num))
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
    result = lib.getAllCameraInfo()
    data = ctypes.string_at(result, -1).decode("utf-8")
    return res_success(data)


@app.route('/check/feature', methods=['GET'])
def check_feature_info():
    image_id = request.args.get('imageId')
    if image_id:
        result = lib.checkFeature(image_id)
        if result == -1:
            return res_fail("检测失败")
        return res_success()
    return res_fail("检测失败")


@app.route('/models', methods=['POST'])
def add_face_model():
    if 'id' in request.json and 'imageId' in request.json and 'isActived' in request.json:
        id = request.json['id']
        imageId = request.json['imageId']
        is_actived = request.json['isActived']
        result = lib.addModel(id, imageId, is_actived)
        if result == 1:
            return res_success()
        else:
            return res_fail("人脸检测失败, 请重新上传")
    return res_fail("请输入正确的参数")


@app.route('/secondModel', methods=['PUT'])
def update_second_model():
    if 'id' in request.json and 'recordId' in request.json:
        id = request.json['id']
        recordId = request.json['recordId']
        result = lib.updateSecondFaceModel(id, recordId)
        if result == 1:
            return res_success()
        else:
            return res_fail()
    return res_fail("请输入正确的参数")


@app.route('/open/door', methods=['POST'])
def open_usb():
    if 'type' in request.json:
        type = request.json['type']
        result = lib.writeFd(type)
        if result == 1:
            return res_success()
        else:
            return res_fail("开门失败")
    return res_fail("请输入正确的参数")


@app.route('/age/test', methods=['POST'])
def age_test():
    if 'id' in request.json and 'attachId' in request.json:
        id = request.json['id']
        attachId = request.json['attachId']
        result = ctypes.c_float()
        lib.ageText(id, attachId, byref(result))
        if result.value != -1:
            return res_success(result.value)
        else:
            return res_fail("开门失败")
    return res_fail("请输入正确的参数")