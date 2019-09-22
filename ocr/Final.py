import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join
#import pytesseract as py
folder_name = 'input_images'
cwd = os.getcwd()
folder_path = os.path.join(cwd,folder_name)
all_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
for file in all_files:
    image_path = os.path.join(folder_path,file)
    image=cv2.imread(image_path)
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imagedenoised=cv2.fastNlMeansDenoising(imgGray,None,3,7,11)
    imgThresh = cv2.adaptiveThreshold(imagedenoised,                           
                                          255,                                  
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       
                                          cv2.THRESH_BINARY_INV,                
                                          11,                                   
                                          2)
    npaContours, npaHierarchy = cv2.findContours(imgThresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    [intX, intY, intW, intH] = cv2.boundingRect(npaContours[0])
    cv2.rectangle(image,(intX, intY),(intX+intW,intY+intH),(0, 0, 255),2)
    for npaContour in npaContours:
        [intX, intY, intW, intH] = cv2.boundingRect(npaContour)
        cv2.rectangle(image,(intX, intY),(intX+intW,intY+intH),(0, 0, 255),2)
        
        
    cv2.imshow('Binary image',image)
    cv2.waitKey(0)