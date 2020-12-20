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
    def tradingTime(date_time, next_day=True):
        if next_day:
            date_time += timedelta(days=1)

        return datetime(date_time.year, date_time.month, date_time.day, 9, 0, 0)

    def tradingTime_(date_time):
        """
        確保時間在交易時間內

        :param date_time:
        :return:
        """
        first_time = datetime(date_time.year, date_time.month, date_time.day, 9, 0, 0)
        last_time = datetime(date_time.year, date_time.month, date_time.day, 13, 30, 0)

        if date_time < first_time:
            date_time = tradingTime(date_time, next_day=False)

        elif date_time > last_time:
            date_time = tradingTime(date_time, next_day=True)

        return date_time

    # 確保先後順序
    if start_time > stop_time:
        temp = start_time
        start_time = stop_time
        stop_time = temp

    # 確保時間在交易時間內
    start_time = tradingTime_(start_time)
    stop_time = tradingTime_(stop_time)
    print(f"start_time: {start_time}, stop_time: {stop_time}")

    curr_time = start_time

    while curr_time <= stop_time:
        yield curr_time
        curr_time = tradingTime_(curr_time + step_time)


if __name__ == "__main__":
    start_time = datetime(2020, 12, 20, 13, 20, 0)
    stop_time = datetime(2020, 12, 22, 13, 30, 3)
    for t in stockTimeRange(start_time=stop_time, stop_time=start_time, step_time=timedelta(minutes=40)):
        print(t)
