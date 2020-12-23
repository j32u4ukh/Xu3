from datetime import datetime, timedelta


def timeRange(start_time: datetime, stop_time: datetime, step_time=timedelta(seconds=1)):
    if start_time > stop_time:
        temp = stop_time
        stop_time = start_time
        start_time = temp

    curr_time = start_time

    while curr_time <= stop_time:
        yield curr_time
        curr_time += step_time


def stockTimeRange(start_time: datetime, stop_time: datetime, step_time=timedelta(seconds=1)):
    # 確保先後順序
    if start_time > stop_time:
        temp = start_time
        start_time = stop_time
        stop_time = temp

    start_time = start_time - timedelta(minutes=1) + timedelta(seconds=1)

    # 確保時間在交易時間內
    start_time = tradingTime(start_time)
    stop_time = tradingTime(stop_time)
    print(f"start_time: {start_time}, stop_time: {stop_time}")

    curr_time = start_time

    while curr_time <= stop_time:
        yield curr_time
        curr_time = tradingTime(curr_time + step_time)


def tradingTimeRange(start_time: datetime, stop_time: datetime, trading_time: list, step_time=timedelta(seconds=1)):
    # 確保先後順序
    if start_time > stop_time:
        temp = start_time
        start_time = stop_time
        stop_time = temp

    trading_time.sort()

    # 確保時間在交易時間內
    start_time = tradingTime(start_time)
    stop_time = tradingTime(stop_time)
    print(f"start_time: {start_time}, stop_time: {stop_time}")

    # 確保時間在交易日期內
    first_date = trading_time[0].date()
    trading_time[0] = datetime(year=first_date.year, month=first_date.month, day=first_date.day,
                               # tick 的時間比 K 棒的時間早 1 分鐘，且從 HH:MM:01 開始計時(若輸入精度到秒，那秒數是不是會怪怪的？)
                               hour=start_time.hour, minute=start_time.minute - 1, second=start_time.second + 1)

    last_date = trading_time[-1].date()
    trading_time[-1] = datetime(year=last_date.year, month=last_date.month, day=last_date.day,
                                hour=stop_time.hour, minute=stop_time.minute, second=stop_time.second)

    n_trade = len(trading_time)

    curr_time = trading_time[0]
    end_time = endTradingTime(curr_time)

    while curr_time <= end_time:
        yield curr_time
        curr_time = tradingTime(curr_time + step_time, next_day=True)

    for t in range(1, n_trade - 1):
        curr_time = trading_time[t]
        curr_time = startTradingTime(curr_time)
        end_time = endTradingTime(curr_time)

        while curr_time <= end_time:
            yield curr_time
            curr_time = tradingTime(curr_time + step_time, next_day=True)

    end_time = trading_time[n_trade - 1]
    curr_time = startTradingTime(end_time)

    while curr_time <= end_time:
        yield curr_time
        curr_time = tradingTime(curr_time + step_time, next_day=True)


def tradingTime(date_time, next_day=False):
    """
    確保時間在交易時間內

    :param date_time:
    :param next_day: 超過交易時間的數值，是否進位到隔天的交易開始時間點
    :return:
    """
    first_time = startTradingTime(date_time)
    last_time = endTradingTime(date_time)

    if date_time < first_time:
        date_time = first_time

    elif date_time > last_time:

        if next_day:
            date_time = first_time + timedelta(days=1)

        else:
            date_time = last_time

    return date_time


def startTradingTime(date_time):
    return datetime(date_time.year, date_time.month, date_time.day, 9, 0, 1)


def endTradingTime(date_time):
    return datetime(date_time.year, date_time.month, date_time.day, 13, 30, 0)


if __name__ == "__main__":
    class Tester:
        def testStockTimeRange(self):
            start_time = datetime(2020, 3, 2, 13, 29)
            stop_time = datetime(2020, 3, 4, 0, 0)
            idx = 0
            for t in stockTimeRange(start_time=stop_time, stop_time=start_time, step_time=timedelta(seconds=1)):
                idx += 1
                print(idx, t)

        def testTradingTime(self):
            date_time = datetime(2020, 3, 2, 8, 45, 0)
            print(f"date_time: {date_time} -> {tradingTime(date_time)}")

            date_time = datetime(2020, 3, 2, 14, 9, 0)
            print(f"date_time: {date_time} -> {tradingTime(date_time)}")

        def testTradingTimeRange(self):
            start_time = datetime(year=2020, month=2, day=20, hour=13, minute=29)
            stop_time = datetime(year=2020, month=3, day=3, hour=9, minute=2)
            trading_time = [datetime(year=2020, month=2, day=20, hour=13, minute=25),
                            datetime(year=2020, month=2, day=26, hour=13, minute=25),
                            datetime(year=2020, month=3, day=3, hour=9, minute=2)]

            """
            0 2020-02-20 13:28:01
            119 2020-02-20 13:30:00
            120 2020-02-26 09:00:01
            16319 2020-02-26 13:30:00
            16320 2020-03-03 09:00:01
            16439 2020-03-03 09:02:00
            """

            idx = 0
            for t in tradingTimeRange(start_time=start_time, stop_time=stop_time, trading_time=trading_time):
                print(idx, t)
                idx += 1


    tester = Tester()
    tester.testTradingTimeRange()
