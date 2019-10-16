import pytesseract
import cv2
import numpy as np
import skimage
def binary(image):
    '''
    Input =  Grayscale image
    OutputBinary Image
    '''
    test_imgThresh = cv2.adaptiveThreshold(image,                           
                                      255,                                  
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       
                                      cv2.THRESH_BINARY_INV,                
                                      11,                                   
                                      2)
    return test_imgThresh


def getcodeinits(image):
    '''
    Input = image
    Output = co_ordinates of connected object
    '''
    npaContours, npaHierarchy = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    codeinits=[]
    for npaContour in npaContours:
        [intX, intY, intW, intH] = cv2.boundingRect(npaContour)
        codeinits.append([intX, intY, intW, intH])
        
    return codeinits

def fetch_string(image):
    '''
    Input = Grayscale image
    Output = Text of a image
    '''
    test_imgThresh=binary(image)
    codeinits=getcodeinits(test_imgThresh)
    final=[]
    for [x,y,w,h] in codeinits:
        dummy=test_imgThresh[y:y+h,x:x+w]
        mserStats =skimage.measure.regionprops(dummy)
        if (mserStats[0]["euler_number"] > -1 or mserStats[0]["euler_number"] <1):
            if(mserStats[0]['Extent'] < 1):
                final.append([x,y,w,h])
    img2=np.zeros((test_imgThresh.shape[0],test_imgThresh.shape[1]),np.uint8)    
    for [x,y,w,h] in final:
        img2[y:y+h,x:x+w]=test_imgThresh[y:y+h,x:x+w]
    config = ('-l eng --oem 1 --psm 11')
    string=pytesseract.image_to_string(img2,config = config)
    return string

