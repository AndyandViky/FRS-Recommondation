
from flask import Flask
from flask import request
import ctypes
ll = ctypes.cdll.LoadLibrary
lib = ll("/home/yanglin/yl/c++/arcsoft-arcface/arcface/src/libface.so")

app = Flask(__name__)

app.debug = True

# lib.initAllEngine()
# lib.openCamera(0)

# middelware #
@app.before_request
def auth():
    if request.method == 'POST':
        auth = request.form['auth']
        if auth == "123":
            pass
        else:
            return "fail"
    else:
        auth = request.args.get('auth')
        if auth == "123":
            pass
        else:
            return "fail"


# router
@app.route('/', methods=['GET'])
def hello_world():

    return "123123"


@app.route('/a')
def hello_world1():
    if request.method == 'POST':
        return "123123"
    else:
        return "123123"