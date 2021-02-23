import inspect
import logging
from logging import handlers
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

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


def getLogger(logger_name, logger_level=logging.DEBUG, instance=False, logger_format=None,
              to_file=True, time_file=False, file_dir: str = "", when='D', max_mb=2, back_count=20, interval=1):
    """

    :param logger_name: logger 名稱
    :param logger_level: logger 的 level
    :param instance: 是否由類別呼叫
    :param logger_format: 輸出格式
    :param to_file: 輸出成檔案
    :param time_file: 是否使用根據時間建立新檔案的輸出格式
    :param file_dir: 輸出資料夾(從最上層開始的相對路徑)
    :param when: 時間間隔的單位
    單位有以下幾種：
    S 秒
    M 分
    H 小時、
    D 天(天的計算似乎會受到開始時間點的影響，明明隔了一天，但計時還未超過 24 小時)、
    W 星期（0=Monday） 'W0'-'W6'
    MIDNIGHT 每天凌晨
    # 參見: https://stackoverflow.com/a/60637138
    :param max_mb: 超過此大小，將會產生同名檔案(不同後綴名稱)
    :param back_count: 備份檔案的個數，如果超過這個個數，就會自動刪除
    :param interval: 時間間隔
    :return:
    """
    if logger_format is None:
        if instance:
            logger_format = '%(asctime)s %(levelname)s: [%(className)s] %(funcName)s | ' \
                            '%(message)s (%(pathname)s, line: %(lineno)d)'
        else:
            logger_format = '%(asctime)s %(levelname)s: %(funcName)s | %(message)s (%(pathname)s, line: %(lineno)d)'

    # logger.debug("debug")
    # logger.info("info")
    # logger.warning("warning")
    # logger.error("error")
    # logger.critical("critical")

    if to_file:
        file_dir = os.path.join("log", file_dir)

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        file_path = os.path.join(file_dir, f"{logger_name}.log")

        if time_file:
            # 創建一個輸出日誌為檔案的 TimedRotatingFileHandler，每間隔固定時間會以時間作為後綴，建立新的輸出檔名
            time_file_handler = handlers.TimedRotatingFileHandler(filename=file_path,
                                                                  interval=interval,
                                                                  when=when,
                                                                  backupCount=back_count,
                                                                  encoding='utf-8')

            logging.basicConfig(format=logger_format, handlers=[logging.StreamHandler(), time_file_handler])

        else:
            file_handler = logging.handlers.RotatingFileHandler(filename=file_path,
                                                                maxBytes=1048576 * max_mb,
                                                                backupCount=back_count,
                                                                encoding='utf-8')

            logging.basicConfig(format=logger_format, handlers=[logging.StreamHandler(), file_handler])

    else:
        logging.basicConfig(format=logger_format, handlers=[logging.StreamHandler()])

    # logger_name: 設置 logger 名稱
    logger = logging.getLogger(logger_name)

    # 設置 logger 的 level
    logger.setLevel(logger_level)

    return logger


if __name__ == "__main__":
    from datetime import datetime

    # getLogger(logger_name, logger_level=logging.DEBUG, logger_format=None, time_file=False,
    #               file_dir="", file_name="", when='D', back_count=20, interval=1)
    logger = getLogger(logger_name=datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
                       logger_level=logging.DEBUG,
                       to_file=True,
                       time_file=False,
                       file_dir="test",
                       instance=True)


    def test():
        d = {"className": "className"}
        for i in range(100):
            logger.debug(i, extra=d)
            # logger.debug(i, extra=d)
            # logger.info(i * 10, extra=d)
            logger.info(i * 10, extra=d)


    test()
