import cv2
import deskew
import imutils

def prepare_image(img):
    img = cv2.GaussianBlur(img, (3,3), 0)
    (thresh, img) = cv2.threshold(img, 128, 255,
                                  cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img = cv2.bitwise_not(img, 0)
    img = imutils.rotate_bound(img, -deskew.calculate(img))
