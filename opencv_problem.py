import cv2
import numpy as np


def problem1():
    # https://www.facebook.com/groups/pythontw/permalink/10159660727668438/
    path = "Xu3/data/china_virus.png"
    img1 = cv2.imread(path)
    img2 = cv2.imread(path, cv2.IMREAD_COLOR)
    img3 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img4 = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    cv2.imshow('image1', img1)
    cv2.imshow('image2', img2)
    cv2.imshow('image3', img3)
    cv2.imshow('image4', img4)

    k = cv2.waitKey(0)

    if k == ord('x'):
        cv2.destroyWindow('image2')

    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()


def problem2_1(full_screen=True):
    # https://www.facebook.com/groups/pythontw/permalink/10159660727668438/
    path = "Xu3/data/china_virus.png"
    window_name = "image"
    img = cv2.imread(path)
    width, height, _ = img.shape

    # cv2.WINDOW_NORMAL: make the window resizable.
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    if full_screen:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, height, width)

    print(cv2.getWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN))

    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def problem2_2():
    # https://www.facebook.com/groups/pythontw/permalink/10159660727668438/
    path = "Xu3/data/china_virus.png"
    img = cv2.imread(path)

    def onChanged(val):
        print(f"Trackbar value: {val}")

    cv2.namedWindow('window_name')

    # Trackbar 名稱，Trackbar 要添加的視窗的名稱，Trackbar 最小值，Trackbar 最大值，數值變動時執行的副程式
    cv2.createTrackbar('trackbar_name', 'window_name', 0, 20, onChanged)
    cv2.setTrackbarMin('trackbar_name', 'window_name', 0)

    cv2.imshow('window_name', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # problem1()
    problem2_1(False)
    # problem2_2()
