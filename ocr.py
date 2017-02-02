from PIL import Image
from pytesseract import *
#import re

def ocr(imgpath = "cache.jpg"):
    img = Image.open(imgpath)
    text = image_to_string(img)
    return(text)
    
if __name__=="__main__":    
    print(ocr("test.png"))
