
from face.bridge import app
import logging
import ctypes

ll = ctypes.cdll.LoadLibrary
lib = ll("/home/yanglin/yl/c++/arcsoft-arcface/arcface/src/libface.so")


if __name__ == '__main__':
    # 初始化引擎
    lib.initAllEngine()

    # 日志配置
    handler = logging.FileHandler('flask2.log', encoding='UTF-8')

    handler.setLevel(logging.DEBUG)

    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

    handler.setFormatter(logging_format)

    app.logger.addHandler(handler)

    app.run(port = 5001)