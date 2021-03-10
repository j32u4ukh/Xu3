import inspect
import logging
from logging import handlers
from functools import total_ordering

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


# 提供 sorted 自定義比較規則，參數可額外添加
def cmpToKey(cmp, **kwargs):
    """修改自 functools.cmp_to_key，參數可額外添加，而不只有要比較的 2 個元素"""

    @total_ordering
    class K(object):
        __slots__ = ['obj']

        def __init__(self, obj):
            self.obj = obj

        def __lt__(self, other):
            return cmp(self.obj, other.obj, **kwargs) < 0

        def __eq__(self, other):
            return cmp(self.obj, other.obj, **kwargs) == 0

        __hash__ = None

    return K


# 倚賴 cmpToKey 才能將此函式傳入 sorted 來自定義比較規則
def keepOrderSorting(value1, value2, **kwargs):
    """
    example:
    sorted(list(zip(indexs, values)), key=cmpToKey(keepOrderSorting, reverse=False)

    :param value1:
    :param value2:
    :param kwargs:
    :return:
    """
    (order1, val1) = value1
    (order1, val2) = value2

    # 沒有 reverse 參數則不反序
    if not kwargs.__contains__("reverse"):
        reverse = False

    # 有 reverse 參數，則根據參數決定是否反序
    else:
        reverse = kwargs["reverse"]

    # 大的排前面
    if reverse:
        if val1 > val2:
            return -1
        elif val1 < val2:
            return 1
        else:
            return 0

    # 小的排前面(一般情況)
    else:
        if val1 < val2:
            return -1
        elif val1 > val2:
            return 1
        else:
            return 0


def sortRank(values, reverse=False):
    """
    數值大小的排名，依照原始順序進行排列。

    :param values:
    :param reverse: 是否由大到小排序
    :return:
    """
    if reverse:
        indexs = list(range(1, len(values) + 1))
        indexs = [index for index, value in sorted(list(zip(indexs, values)),
                                                   key=cmpToKey(keepOrderSorting, reverse=True))]

        ranks = list(range(1, len(indexs) + 1))
        ranks = [rank for rank, index in sorted(list(zip(ranks, indexs)),
                                                key=cmpToKey(keepOrderSorting, reverse=False))]
    else:
        # 索引值(indexs) 先隨著 數值(values) 進行排序
        indexs = list(range(1, len(values) + 1))
        indexs = [index for index, value in sorted(list(zip(indexs, values)),
                                                   key=cmpToKey(keepOrderSorting, reverse=False))]

        # 排名(ranks) 再隨著 依數值大小排序過的索引值(indexs) 進行排序
        ranks = list(range(1, len(indexs) + 1))
        ranks = [rank for rank, index in sorted(list(zip(ranks, indexs)),
                                                key=cmpToKey(keepOrderSorting, reverse=False))]

    return ranks


def selectMultiColumns(df, column_indexs: list):
    names = [name for i, name in enumerate(df.columns) if i in column_indexs]
    select_columns = df[names]

    return select_columns, names


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
