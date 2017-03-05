from functools import reduce
import cv2
import deskew
import imutils
import numpy as np

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

# Kept here for Lega-pitek-cy reasons
def contours_edges_old(img, contours):
    minx = img.shape[1]
    maxx = 0
    miny = img.shape[0]
    maxy = 0
    for e in contours:
        for f in e:
            for g in f:
                minx = min(minx, g[0])
                maxx = max(maxx, g[0])
                miny = min(miny, g[1])
                maxy = max(maxy, g[1])
    miny -= 10
    minx -= 10
    maxy += 10
    maxx += 10
    if miny < 0:
        miny = 0
    if minx < 0:
        minx = 0
    if maxy > img.shape[0]:
        maxy = img.shape[0]
    if maxx > img.shape[1]:
        maxx = img.shape[1]
    return minx, miny, maxx, maxy

def contours_edges(img, contours):
    h, w = img.shape
    transformed = [tuple(min(sub.flatten().reshape(-1, 2), key=sum)) for sub in contours]
    x_vals = reduce(np.union1d, [array.flatten()[::2]  for array in contours])
    y_vals = reduce(np.union1d, [array.flatten()[1::2] for array in contours])
    minx, miny, maxx, maxy = x_vals[0], y_vals[0], x_vals[-1], y_vals[-1]
    minx = max(minx - 10, 0); miny = max(miny - 10, 0)
    maxx = min(maxx + 10, w); maxy = min(maxy + 10, h)
    return minx, miny, maxx, maxy

def prepare_image(img, dodeskew=True, height=200):
    # Threshold
    thresh, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Bitwise not    
    img = cv2.bitwise_not(img, 0)
    # Deskewing
    if dodeskew:
        angle = deskew.calculate(img)
        while abs(angle) > 15:
            img = imutils.rotate_bound(img, -angle)
            angle = deskew.calculate(img)
    # Crop
    im2, contours, hierarchy = cv2.findContours(img,1,2)
    minx, miny, maxx, maxy = contours_edges(img, contours)
    img = img[miny:maxy, minx:maxx]
    # Resize
    img = relative_resize_h(img, height)
    # Revert bitwise not
    img = cv2.bitwise_not(img)

    return img
