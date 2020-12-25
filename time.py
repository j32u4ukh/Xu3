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
    print(f"[tradingTimeRange] trading_time: {trading_time}")

    first_date = trading_time[0].date()

    # start_time 這天沒有交易
    if start_time.date() < first_date:
        print(f"[tradingTimeRange] first_date: {first_date}, start_time.date(): {start_time.date()}")
        start_time = datetime(year=first_date.year, month=first_date.month, day=first_date.day,
                              hour=9, minute=0, second=0)

    # start_time 是有交易的日子
    else:
        print(f"[tradingTimeRange] start_time before modify: {start_time}")
        # tick 的時間比 K 棒的時間早 1 分鐘，且從 HH:MM:01 開始計時(若輸入精度到秒，那秒數是不是會怪怪的？)
        start_time = start_time - timedelta(minutes=1) + timedelta(seconds=1)
        print(f"[tradingTimeRange] start_time: {start_time}")

    start_time = tradingTime(start_time)
    print(f"[tradingTimeRange] start_time after tradingTime: {start_time}")

    last_date = trading_time[-1].date()

    # stop_time 這天沒有交易
    if last_date < stop_time.date():
        print(f"[tradingTimeRange] last_date: {last_date}, stop_time.date(): {stop_time.date()}")
        stop_time = datetime(year=last_date.year, month=last_date.month, day=last_date.day,
                             hour=13, minute=30, second=0)

    # stop_time 是有交易的日子
    else:
        first_stop_time = startTradingTime(stop_time)
        print(f"[tradingTimeRange] first_stop_time: {first_stop_time}")

        # 若結束時間的指定，並不在最後一天的交易時間內，表示想要到前一天的交易結束時間點
        if stop_time < first_stop_time:
            stop_time = endTradingTime(stop_time - datetime.timedelta(days=1))
            print(f"[tradingTimeRange] stop_time -> last day endTradingTime: {stop_time}")

    stop_time = tradingTime(stop_time)

    print(f"[tradingTimeRange] start_time: {start_time}, stop_time: {stop_time}")

    n_trading_time = len(trading_time)

    if n_trading_time == 1:
        start_trading = start_time
        end_trading = stop_time
        curr_time = start_trading

        while curr_time <= end_trading:
            yield curr_time
            curr_time = tradingTime(curr_time + step_time, next_day=True)

    elif n_trading_time == 2:
        # 第一天
        start_trading = start_time
        end_trading = endTradingTime(start_time)
        curr_time = start_trading

        while curr_time <= end_trading:
            yield curr_time
            curr_time = tradingTime(curr_time + step_time, next_day=True)

        start_trading = startTradingTime(stop_time)
        end_trading = stop_time
        curr_time = start_trading

        # 最後一天
        while curr_time <= end_trading:
            yield curr_time
            curr_time = tradingTime(curr_time + step_time, next_day=True)

    else:
        # 第 1 天
        start_trading = start_time
        end_trading = endTradingTime(start_time)
        curr_time = start_trading

        while curr_time <= end_trading:
            yield curr_time
            curr_time = tradingTime(curr_time + step_time, next_day=True)

        # 第 2 天 ~ 第 N - 1 天
        for i in range(1, n_trading_time - 1):
            date_time = trading_time[i]
            start_trading = startTradingTime(date_time)
            end_trading = endTradingTime(date_time)
            curr_time = start_trading

            while curr_time <= end_trading:
                yield curr_time
                curr_time = tradingTime(curr_time + step_time, next_day=True)

        start_trading = startTradingTime(stop_time)
        end_trading = stop_time
        curr_time = start_trading

        # 第 N 天(最後一天)
        while curr_time <= end_trading:
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
            start_time = startTradingTime(datetime(2020, 5, 14))
            stop_time = endTradingTime(datetime(2020, 5, 21))
            trading_time = [datetime(year=2020, month=5, day=15),
                            datetime(year=2020, month=5, day=17),
                            datetime(year=2020, month=5, day=19),
                            datetime(year=2020, month=5, day=21)]

            """

            """

            idx = 0
            for t in tradingTimeRange(start_time=start_time, stop_time=stop_time, trading_time=trading_time,
                                      step_time=timedelta(minutes=1)):
                if idx % 30 == 0:
                    print(idx, t)

                idx += 1


    tester = Tester()
    tester.testTradingTimeRange()
