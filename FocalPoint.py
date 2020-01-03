import cv2


img = cv2.imread("data/open_eyes1.png", cv2.IMREAD_GRAYSCALE)
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

kernal_shape = (9, 16)
predict_shape = (27, 48)
standard_shape = (63, 112)

img_height, img_width = img.shape
standard_height, standard_width = standard_shape
