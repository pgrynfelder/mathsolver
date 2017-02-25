from string import ascii_lowercase as letters

import pyocr
import sympy as sp
from PIL import Image
import cv2
import numpy as np

import img_from_phone
import imgformat
import text_utils
import sympy_utils

#Identifier for solve call with image from phone camera
FROM_PHONE = object()  

#after the star are keyword arguments ~Kubin (delete this when merging)

def read_solve(filename=FROM_PHONE,
               *,
               tool=pyocr.tesseract,
               phone_dir="storage/emulated/0/DCIM/Camera",
               ocr_lang="eng"):
    TEMP = "cache.png"
    print("===Start reading===")
    if filename is FROM_PHONE:
        img_from_phone.load(phone_dir, TEMP)
        img = cv2.imread(TEMP, 0)
    else:
        img = cv2.imread(filename, 0)
    # Check if the image loaded correctly
    if not img.any():
        raise FileNotFoundError("Invalid image filename")

    imgformat.prepare_image(img)
    cv2.imwrite(TEMP, img)
    img = Image.open(TEMP)
    preformatted_text = tool.image_to_string(img, lang=ocr_lang)
        
    if not preformatted_text:
        raise ValueError("Cannot find any text in image")
    
    try:
        print("Preformatted text:", preformatted_text)
    except UnicodeEncodeError:
        print("[...] (Couldn't encode characters in terminal)")


    print("---Format input---") 
    text = preformatted_text
    
    # Common OCR mistakes
    text = text_utils.casefix(text)
    text = text_utils.fix_common_mistakes(text)
    text = text_utils.fix_syntax_mistakes(text)
        
    # Create left and right side of equation
    split = text.split("=")
    if len(split) == 1:
        text1, text2 = split[0], "0"
    elif len(split) == 2:
        text1, text2 = split
    else:
        raise ValueError("Found {} equality signs, max is 1".format(len(split)))
        
    # Extract the variable in the equation
    vars1 = text_utils.find_variables(text1)
    vars2 = text_utils.find_variables(text2)
    # Get both the left and right side
    variables = list(set(vars1) | set(vars2))

    print("===Start computing===")
    expr1 = sympy_utils.simple_expr_parse(text1)
    expr2 = sympy_utils.simple_expr_parse(text2)
    
    print("The equation: {} = {}".format(expr1, expr2))
    result = sympy_utils.simple_solve(expr1, expr2, variables)
    print("Result: {}".format(result))
    return result

if __name__ == "__main__":
    tests = ["3x.png", "test3.png", "test4.png", "example2.jpg"]
    for test in tests:
        result = read_solve(test)
        print(result, "\n\n")
