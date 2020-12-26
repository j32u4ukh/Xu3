import inspect
import logging
from logging import handlers
import cv2
import os


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


def getLogger(logger_name, logger_level=logging.DEBUG, logger_format=None, time_file=False, file_dir="",
              when='D', back_count=20, interval=1):
    """

    :param logger_name: logger 名稱
    :param logger_level: logger 的 level
    :param logger_format: 輸出格式
    :param time_file: 是否使用根據時間建立新檔案的輸出格式
    :param file_dir: 輸出資料夾(從最上層開始的相對路徑)
    :param when: 時間間隔的單位
    單位有以下幾種：
    S 秒
    M 分
    H 小時、
    D 天、
    W 星期（0=Monday） 'W0'-'W6'
    MIDNIGHT 每天凌晨
    :param back_count: 備份檔案的個數，如果超過這個個數，就會自動刪除
    :param interval: 時間間隔
    :return:
    """
    if logger_format is None:
        logger_format = '%(asctime)s %(levelname)s: [%(name)s] %(funcName)s | ' \
                        '%(message)s (line: %(lineno)d, %(pathname)s)'

    # logger.debug("debug")
    # logger.info("info")
    # logger.warning("warning")
    # logger.error("error")
    # logger.critical("critical")

    # logger_name: 設置 logger 名稱
    logger = logging.getLogger(logger_name)

    # 設置 logger 的格式
    formatter = logging.Formatter(logger_format)

    # 設置 logger 的 level
    logger.setLevel(logger_level)

    # 避免重複輸出 log
    if not logger.handlers:
        # 創建一個輸出日誌到控制台的 StreamHandler
        console_handler = logging.StreamHandler()

        # 將格式添加給 StreamHandler
        console_handler.setFormatter(formatter)

        # 將 handler 添加給 logger
        logger.addHandler(console_handler)

        if time_file:
            file_dir = os.path.join("log", file_dir)

            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            file_name = os.path.join(file_dir, f"{logger_name}.log")

            # 創建一個輸出日誌為檔案的 TimedRotatingFileHandler，每間隔固定時間會以時間作為後綴，建立新的輸出檔名
            time_file_handler = handlers.TimedRotatingFileHandler(filename=file_name,
                                                                  interval=interval,
                                                                  when=when,
                                                                  backupCount=back_count,
                                                                  encoding='utf-8')

            # 將格式添加給 TimedRotatingFileHandler
            time_file_handler.setFormatter(formatter)

            # 將 handler 添加給 logger
            logger.addHandler(time_file_handler)

    return logger


if __name__ == "__main__":
    logger = getLogger("Xu3", logging.DEBUG, time_file=True, file_dir="test", when='S', interval=2, back_count=2)

    def test():
        from time import time, sleep

        for i in range(20):
            logger.debug(i)
            logger.info(i * 10)
            # print(i)
            sleep(0.5)


    test()
