import cv2
import numpy as np
import sympy

def calculate(img):
    edges = cv2.Canny(img,10,10)

    angles = []

    lines = cv2.HoughLines(edges,1,np.pi/180,5)
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        #print(rho,theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        c,d = sympy.symbols('c d')
        solution = sympy.solve([c * x1 + d - y1, c * x2 + d - y2], c, d)
        #print(solution)
        if not solution:
            angle = 90
        else:
            angle = np.arctan(float(solution[c]))
        angles.append(np.degrees(angle))
        #print("deskewing angle:", angles)

        #cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    return(angles[0])
