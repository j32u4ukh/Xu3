import threading
import time
from abc import ABCMeta, abstractmethod

from submodule.events import Event


class Job(threading.Thread, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()

        # 用於暫停執行緒的標識
        self.__flag = threading.Event()

        # 設定為 True
        self.__flag.set()

        # 用於停止執行緒的標識
        self.__running = threading.Event()

        # 將 running 設定為 True
        self.__running.set()

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    # 若為 False，則持續等待，直到變成 True
    def checkPause(self):
        self.__flag.wait()

    def pause(self):
        # 設定為 False, 讓執行緒阻塞
        self.__flag.clear()

    def resume(self):
        # 設定為 True, 讓執行緒停止阻塞
        self.__flag.set()

    def stop(self):
        # 將執行緒從暫停狀態恢復, 如何已經暫停的話
        self.__flag.set()

        # 設定為 False
        self.__running.clear()


if __name__ == "__main__":
    class TestJob(Job):
        def __init__(self, index):
            super().__init__()
            self.index = index

        def run(self):
            for i in range(20):
                self.checkPause()
                print(f"{self.index}: {i}\n")
                time.sleep(1)


    class Job1(Job):
        def __init__(self, index, onPause, onResume):
            super().__init__()
            self.index = index
            self.onPause = onPause
            self.onResume = onResume

        def run(self):
            for i in range(20):
                self.checkPause()

                if i == 8:
                    self.onPause(index=self.index)

                if i == 12:
                    self.onResume(index=self.index)

                print(f"{self.index}: {i}")
                time.sleep(1)


    class Job2(Job):
        def __init__(self, index, onPause, onResume):
            super().__init__()
            self.index = index
            self.onPause = onPause
            self.onResume = onResume

        def run(self):
            for i in range(20):
                self.checkPause()
                print(f"{self.index}: {i}")
                time.sleep(1)


    class MultiJob:
        def __init__(self):
            self.event = Event()
            self.onPause = self.event.onPause
            self.onResume = self.event.onResume

            self.job1 = Job1(index=0, onPause=self.onPause, onResume=self.onResume)
            self.job2 = Job2(index=1, onPause=self.onPause, onResume=self.onResume)
            self.jobs = [self.job1, self.job2]

            self.onPause += self.onPauseListener
            self.onResume += self.onResumeListener

        def run(self):
            for job in self.jobs:
                job.start()

        def onPauseListener(self, index):
            for job in self.jobs:
                if job.index == index:
                    continue

                job.pause()

        def onResumeListener(self, index):
            for job in self.jobs:
                if job.index == index:
                    continue

                job.resume()


    def testJob():
        job = TestJob(index=1)
        job.start()

        for i in range(20):
            if i == 8:
                job.pause()
            elif i == 12:
                job.resume()

            print(f"0: {i}\n")
            time.sleep(1)


    def testMultiJob():
        mj = MultiJob()
        mj.run()


    # testJob()
    testMultiJob()
