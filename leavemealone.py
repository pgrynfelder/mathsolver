import pyocr
import sympy as sp
from PIL import Image
import imutils
import deskew
import cv2
import getimage
import numpy as np

def solve(filename = ""):
    TEMP = "cache.png"
    tool = pyocr.tesseract
    if filename == "":
        getimage.load("storage/emulated/0/DCIM/Camera", TEMP)
        img = cv2.imread(TEMP, 0)
        #print("image pulled from phone")
    else:
        img = cv2.imread(filename, 0)
        #print("image filename:", filename)
    #checking if the img loaded
    if not img.any():
        print("Please pass a valid image filename")
        return None
    img = cv2.GaussianBlur(img, (3,3), 0)
    (thresh, img) = cv2.threshold(img, 128, 255,
                                  cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img = cv2.bitwise_not(img, 0)
    img = imutils.rotate_bound(img, -deskew.calculate(img))
    cv2.imwrite(TEMP, img)
    
    img = Image.open(TEMP)
    text = tool.image_to_string(
        img,
        lang = "eng"
    )
    if not text:
        print("Cannot find any text")
        return None
    #print("before formatting:", text)

    #mistakes elimination
    text.casefold
    mistakes = {'"': '^',
                '“': '^',
                ' ': '',
                ':': '=',
                'A': '^',
                '-+': '+',
                '¢': '*',
                'O': '0',
                '—': '-'}
                
    for mistake in mistakes:
        text = text.replace(mistake, mistakes[mistake])
    #print("after formatting: ", text)
    #conversion to sympy syntax
    symbols = {'^': '**'}
    for symbol in symbols:
        text = text.replace(symbol, symbols[symbol])
    #print("after syntax conversion:", text)
    #create left and right side of eq
    if "=" in text:
        text1, text2 = text.split("=")
    else:
        text1, text2 = text, "0"
    #extract the variable
    letters = "qwertyuiopasdfghjklzxcvbnm"
    variables = []
    for l in text1:
        if l in letters:
            if l not in variables:
                variables.append(l)
    transformations = (sp.parsing.sympy_parser.standard_transformations +
                      (sp.parsing.sympy_parser.implicit_multiplication_application,
                       )
                       )
    expr1 = sp.parsing.sympy_parser.parse_expr(text1,
                                               transformations = transformations,
                                               evaluate = 0)
    expr2 = sp.parsing.sympy_parser.parse_expr(text2,
                                               transformations = transformations,
                                               evaluate = 0)
    print("The equation:", expr1, "=", expr2)
    return sp.solveset(sp.Eq(expr1, expr2), sp.Symbol(variables[0]), domain = sp.S.Reals)
print(solve("3x.png"))
print(solve("test3.png"))
print(solve("test4.png"))
print(solve("example2.jpg"))
