import cv2
import deskew
import imutils

def cv_size(img):
    return img.shape[1::-1]

def relative_resize_w(img, towidth):
    width, height = cv_size(img)
    ratio = towidth / width
    toheight = int(ratio * height)
    return cv2.resize(img, (towidth, toheight))

def relative_resize_h(img, toheight):
    width, height = cv_size(img)
    ratio = toheight / height
    towidth = int(ratio * width)
    return cv2.resize(img, (towidth, toheight))
    
def prepare_image(img, dodeskew=True, height=100):
    #img = cv2.GaussianBlur(img, (3,3), 0)
    thresh, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if dodeskew:
        img = cv2.bitwise_not(img, 0)
        img = imutils.rotate_bound(img, -deskew.calculate(img))
        img = cv2.bitwise_not(img, 0)
    img = relative_resize_h(img, height)
    return img
