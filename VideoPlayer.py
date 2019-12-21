import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

import cv2


class VideoPlayer:
    def __init__(self, _path):
        self.path = _path
        self.cap = None
        self.index = 0
        self.frames = 0
        self.keep_playing = False
        self.is_searching = False
        self.wait_time = 1
        self.plus_more = 10
        self.minus_more = 10

        # region For split video
        self.output = None
        self.split_index = []
        self.group_index = []
        # endregion

        self.func = {ord(' '): self.pauseOrPlay,
                     ord(','): self.minus1,
                     ord('m'): self.minusMore,
                     ord('.'): self.plus1,
                     ord('/'): self.plusMore,
                     27: self.stop}

        self.getFrames()

    def getFrames(self):
        self.cap = cv2.VideoCapture(self.path)
        self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("Toatl frames number is ", self.frames)

    def play(self):
        # Create a window
        cv2.namedWindow('play')

        # create trackbars for playing
        cv2.createTrackbar('speed', 'play', 1, 50, self.nothing)
        cv2.setTrackbarMin('speed', 'play', 1)
        cv2.createTrackbar('jump', 'play', 10, 50, self.nothing)
        cv2.setTrackbarMin('jump', 'play', 2)

        self.index = 0
        self.cap = cv2.VideoCapture(self.path)
        self.keep_playing = True

        while self.keep_playing:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.index)
            _ret, _frame = self.cap.read()

            if not _ret:
                break
            else:
                cv2.imshow("play", _frame)
                self.plus_more = cv2.getTrackbarPos('jump', 'play')
                self.minus_more = cv2.getTrackbarPos('jump', 'play')

                if self.is_searching:
                    key_code = cv2.waitKey(0)
                    # print("key_code:", key_code)
                else:
                    key_code = cv2.waitKey(1)

                # region Feedback to key_code
                if self.func.__contains__(key_code):
                    self.func.get(key_code)()
                elif 48 <= key_code <= 57:
                    self.split_index.append(self.index)
                    self.group_index.append(key_code - 48)
                # endregion

                if not self.is_searching:
                    self.index += cv2.getTrackbarPos('speed', 'play')

        self.cap.release()
        cv2.destroyAllWindows()

    def splitVideo(self, _output_path):
        if len(self.split_index) != 0:
            self.split_index.append(self.frames)
            self.group_index.append(0)
            self.index = 0
            self.cap = cv2.VideoCapture(self.path)

            # 取得影像的尺寸大小
            _width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            _height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # 使用 XVID 編碼
            _fourcc = cv2.VideoWriter_fourcc(*'XVID')

            # 取得影片幀率
            _fps = self.cap.get(cv2.CAP_PROP_FPS)

            _video_num = 0
            _count = len(self.group_index)

            # 檔案名稱
            _file_name = datetime.now().strftime("%Y%m%d%H%M%S%f")

            # 輸出類別資料夾
            _output_class = self.group_index[_video_num]
            _output = os.path.join(_output_path, str(_output_class))

            # 輸出最後一幀之索引值
            _end_index = self.split_index[_video_num]

            # 確保資料夾存在
            if not os.path.exists(_output):
                os.makedirs(_output)

            # 影片寫出
            self.output = cv2.VideoWriter('{}/{}.mp4'.format(_output, _file_name),
                                          _fourcc,
                                          _fps,
                                          (_width, _height))

            while self.cap.isOpened():
                _ret, _frame = self.cap.read()

                if not _ret:
                    break
                else:
                    if self.index <= _end_index:
                        # 寫入影格
                        self.output.write(_frame)
                        self.index += 1
                    else:
                        # 釋放所有資源
                        self.output.release()

                        # 指向下一段影片
                        _video_num += 1

                        # 判斷是否已是最後一段，是則更新輸出所需資訊
                        if _video_num <= _count - 1:
                            # 檔案名稱
                            _file_name = datetime.now().strftime("%Y%m%d%H%M%S%f")

                            # 輸出類別資料夾
                            _output_class = self.group_index[_video_num]
                            _output = os.path.join(_output_path, str(_output_class))

                            # 輸出最後一幀之索引值
                            _end_index = self.split_index[_video_num]

                            # 確保資料夾存在
                            if not os.path.exists(_output):
                                os.makedirs(_output)

                            # 影片寫出
                            self.output = cv2.VideoWriter('{}/{}.mp4'.format(_output, _file_name),
                                                          _fourcc,
                                                          _fps,
                                                          (_width, _height))
                        else:
                            break

            # 釋放所有資源
            self.cap.release()
            self.output.release()

    def stop(self):
        self.keep_playing = False

    def plus(self, _number):
        if self.index + _number < self.frames:
            self.index += _number
        else:
            self.index = self.frames - 1

        print("Current index:", self.index)

    def plus1(self):
        self.plus(1)

    def plusMore(self):
        self.plus(self.plus_more)

    def minus(self, _number):
        if self.index - _number >= 0:
            self.index -= _number
        else:
            self.index = 0

        print("Current index:", self.index)

    def minus1(self):
        self.minus(1)

    def minusMore(self):
        self.minus(self.minus_more)

    def pauseOrPlay(self):
        self.is_searching = not self.is_searching

    def nothing(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    # 利用彈出視窗，選擇輸入檔案
    input_path = filedialog.askopenfilename()

    if input_path != "":
        print("input_path:", input_path)
        vp = VideoPlayer(input_path)
        vp.play()
        vp.splitVideo("j32u4ukh/data/SplitData")

        print("split_index:", vp.split_index)
        print("group_index:", vp.group_index)
