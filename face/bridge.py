
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


# router
@app.route('/camera', methods=['PUT'])
def open_camera():
    if 'cameraNum' not in request.json:
        return res_fail("摄像头编号不能为空")
    camera_num = request.json["cameraNum"]
    result = lib.openCamera(camera_num)
    if result == -1:
        return res_fail("开启失败")
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


@app.route('/door', methods=['POST'])
def open_usb():
    if 'type' in request.json:
        type = request.json['id']
        result = lib.writeFd(type)
        if result == 1:
            return res_success()
        else:
            return res_fail()
    return res_fail("请输入正确的参数")