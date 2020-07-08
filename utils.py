import cv2
import inspect
import logging


def showImage(*args):
    for _index, _arg in enumerate(args):
        cv2.imshow("img {}".format(_index), _arg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def showImages(**kwargs):
    for _key in kwargs:
        cv2.imshow("{}".format(_key), kwargs[_key])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def multiOperation(op, *args):
    result = args[0]
    length = len(args)

    for i in range(1, length):
        result = op(result, args[i])

    return result


def getFuncName():
    return inspect.stack()[1][3]


def getLogger(logger_name, logger_level=logging.DEBUG, logger_format=None):
    if logger_format is None:
        logger_format = '%(asctime)s [%(name)s] %(levelname)s: %(funcName)s | ' \
                        '%(message)s (%(pathname)s, line: %(lineno)d)'

    # logger.debug("debug")
    # logger.info("info")
    # logger.warning("warning")
    # logger.error("error")
    # logger.critical("critical")

    # logger_name: 設置 logger 名稱
    logger = logging.getLogger(logger_name)

    # 避免重複輸出 log
    if not logger.handlers:
        # 設置 logger 的 level
        logger.setLevel(logger_level)

        # 創建一個輸出日誌到控制台的 StreamHandler
        handler = logging.StreamHandler()

        # 設置 logger 的格式
        formatter = logging.Formatter(logger_format)

        # 將格式添加給 StreamHandler
        handler.setFormatter(formatter)

        # 將 handler 添加給 logger
        logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    logger = getLogger("Xu3", logging.DEBUG)

    def test():
        print("Function")
        # func_name = getFuncName()
        logger.debug("Function")


    test()
