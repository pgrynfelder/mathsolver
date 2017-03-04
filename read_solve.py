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

NOPRINT = lambda *args, **kwargs: None
CPRINT = print

def full_read(filename, *, tool=pyocr.tesseract, phone_dir="storage/emulated/0/DCIM/Camera",
                           ocr_lang="eng", doprint=True):
    if not doprint: print = NOPRINT
    else:           print = CPRINT
    print("===Start reading===")
    TEMP = "cache.png"
    if filename is FROM_PHONE:
        img_from_phone.load(phone_dir, TEMP)
        img = cv2.imread(TEMP, 0)
    else:
        img = cv2.imread(filename, 0)
    # Check if the image loaded correctly
    if not img.any():
        raise FileNotFoundError("Invalid image filename")

    img = imgformat.prepare_image(img, False)
    cv2.imwrite(TEMP, img); imgt = Image.open(TEMP)
    preformatted_text = tool.image_to_string(imgt, lang=ocr_lang)  
    if not preformatted_text:
        raise ValueError("Could not find any text in image")
    
    try:
        print("Preformatted text:", preformatted_text)
    except UnicodeEncodeError:
        print("[...] (Couldn't encode characters in terminal)")


    print("---Format input---") 
    text = preformatted_text

    return text

    
def full_solve(text, *, doprint=True):
    if not doprint: print = NOPRINT
    else:           print = CPRINT
    # Common OCR mistakes
    text = text_utils.fix_common_mistakes(text)
    text = text_utils.fix_syntax_mistakes(text)
    text = text_utils.casefix(text)
    text = text_utils.fix_exponentation(text)

    # Left and right side of the equation
    text1, text2 = text_utils.find_equation_sides(text)
        
    # Extract the variable in the equation
    vars1 = text_utils.find_variables(text1)
    vars2 = text_utils.find_variables(text2)
    # Get both the left and right side
    variables = list(set(vars1) | set(vars2))
    print("===Start computing===")
    expr1 = sympy_utils.simple_expr_parse(text1)
    expr2 = sympy_utils.simple_expr_parse(text2)
    
    print("The equation: {} = {}".format(expr1, expr2))
    if not variables:
        if sp.simplify(expr1) == sp.simplify(expr2):
            return sp.S.Reals
        else:
            return sp.EmptySet()
    result = sympy_utils.simple_solve(expr1, expr2, variables)
    print("Result: {}".format(result))
    return result

def read_solve(filename, *, tool=pyocr.tesseract, phone_dir="storage/emulated/0/DCIM/Camera",
                            ocr_lang="eng", doprint=True):
    text = full_read(filename, tool=tool, phone_dir=phone_dir, ocr_lang=ocr_lang, doprint=doprint)
    result = full_solve(text, doprint=doprint)
    
    return result

testing_files = False
testing_fromphone = False
testing_edgecases = False

if __name__ == "__main__":
    if testing_files:
        tests = ["3x.png", "test3.png", "test4.png",
                 "example1.jpg", "example2.jpg"]
        for test in tests:
            result = read_solve(test)
            print(result, "\n\n")
            input("Press enter...\n\n")
    if testing_fromphone:
        result = read_solve(FROM_PHONE)
        print(result)
    if testing_edgecases:
        result1 = full_solve("0 = 1")
        result2 = full_solve("0 = 0")
        print(result1, result2)
