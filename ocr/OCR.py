import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join
def convert_to_binary(image):
    blur = cv2.GaussianBlur(image,(5,3), 1)
    imgGray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    imagedenoised=cv2.fastNlMeansDenoising(imgGray,None,3,7,11)
    imgThresh = cv2.adaptiveThreshold(imagedenoised,                           
                                      255,                                  
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       
                                      cv2.THRESH_BINARY_INV,                
                                      11,                                   
                                      2)
    return imgThresh


def react(codeinits):
    for itx,(xmin,ymin,width,height) in enumerate(codeinits):
        cv2.rectangle(image,(xmin,ymin),(xmin+width,ymin+height),(0,255,0),2)



def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
     
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
    	angle = -(90 + angle)
     
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
    	angle = -angle
        
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    # draw the correction angle on the image so we can validate it
    
    return rotated
    
    
    
   

def Sort_word(sub_li): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    return(sorted(sub_li, key = lambda x: x[0])) 
    
    

def getHorizontalProjectionProfile(image): 
    image[image == 0]   = 1
    image[image == 255] = 0
    horizontal_projection = np.sum(image, axis = 1)  
    return horizontal_projection 


def getVerticalProjectionProfile(image):
    image[image == 0]   = 1
    image[image == 255] = 0
    vertical_projection = np.sum(image ,axis = 0)
    return vertical_projection


def getcodeinits(image):
    npaContours, npaHierarchy = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#Getting values x,y,w,h of each pixel in the connected object
    linecodeinits=[]
    for npaContour in npaContours:
        [intX, intY, intW, intH] = cv2.boundingRect(npaContour)
        linecodeinits.append([intX, intY, intW, intH])
        
    return linecodeinits


def Sort_line(sub_li): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    return(sorted(sub_li, key = lambda x: x[1])) 
    


############################################################################################
def getcodeinitsword(image,ymin,height):
    npaContours, npaHierarchy = cv2.findContours(image, 
                                                 cv2.RETR_EXTERNAL, 
                                                 cv2.CHAIN_APPROX_SIMPLE
                                                 )#Getting values x,y,w,h of each pixel in the connected object
    codeinits=[]
    for npaContour in npaContours:
        [intX, intY, intW, intH] = cv2.boundingRect(npaContour)
        codeinits.append([intX, ymin, intW, height])
        
    return codeinits


def createrightreactangle_word(codeinits):
    #codeinits=Sort_line(codeinits)
    final=[]
    for i in range(0,len(codeinits)):
        if(i == 0) and codeinits[i+1]:
            q=codeinits[i+1]
            ymin0=codeinits[i][0]
            ymax0=ymin0+codeinits[i][2]
            ymin1=q[0]
            p=ymin1-ymax0
            a=[]
            if(p<8):
                a.append(codeinits[i][0])
                a.append(codeinits[i][1])
                a.append(codeinits[i][2]+p+q[2])
                a.append(codeinits[i][3])
                final.append(a)
            else:
                final.append(codeinits[i])
        else:
            ymin0=final[len(final)-1][0]
            ymax0=ymin0+final[len(final)-1][2]
            ymin1=codeinits[i][0]
            p=ymin1-ymax0
            a=[]
            if(p<8):
                a.append(final[len(final)-1][0])
                a.append(final[len(final)-1][1])
                a.append(final[len(final)-1][2]+p+codeinits[i][2])
                a.append(final[len(final)-1][3])
                final.pop()
                final.append(a)
            else:
                final.append(codeinits[i])
                
    print(final)
    return final



def getwordcodeinits(image,ymin,height):
    finalcodeinits=[]
    dummyimage=np.zeros((image.shape[0],image.shape[1]),np.uint8)
    vertical_projection=getVerticalProjectionProfile(image)
    
    lsts=[]   
    for idx, bound in enumerate(vertical_projection):
        if bound != dummy.shape[0]:
            lsts.append(idx)
    for i in lsts:
        cv2.line(dummyimage, (i, 0), (i, dummy.shape[0]), (255,255,255), 2)
    finalcodeinits.append(getcodeinitsword(dummyimage,ymin,height))
    return finalcodeinits


if __name__ == '__main__':
    folder_name = 'input_images'
    cwd = os.getcwd()
    folder_path = os.path.join(cwd,folder_name)
    all_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    for file in all_files:
        image_path = os.path.join(folder_path,file)
        image=cv2.imread(image_path)
        image=deskew(image)
        image=cv2.resize(image,(1024,1024))
        img=np.zeros((image.shape[0],image.shape[1]),np.uint8)
        imgThresh=convert_to_binary(image)
        horizontal_projection = getHorizontalProjectionProfile(imgThresh.copy()) 
        lst=[]   
        for idx, bound in enumerate(horizontal_projection):
            if bound != image.shape[1] :
                lst.append(idx)
              
        for i in lst:
            cv2.line(img, (0, i), (image.shape[1], i), (255,255,255), 2)
            
        linecodeinits=getcodeinits(img)
        len(linecodeinits)
        a=[]
        for [intX, intY, intW, intH] in linecodeinits:
            dummy=imgThresh[intY:intY+intH,intX:intX+intW]
            a.append(getwordcodeinits(dummy,intY,intH))
        
        
        wordcodeinits=[]   
        for i in range(0,len(a)):
            wordcodeinits.append(Sort_word(a[i][0]))    
        
        wordcodeinits 
        
        finalcodeinits=[]
        for i in range(0,len(wordcodeinits)):
            print(wordcodeinits[i])
            print(len(wordcodeinits[i]))
            mini=len(wordcodeinits[i])
            if (mini > 1):
                finalcodeinits.append(createrightreactangle_word(wordcodeinits[i]))
            else:
                finalcodeinits.append(wordcodeinits[i])
        
        
        len(finalcodeinits)
        for i in range(0,len(finalcodeinits)):
            print(finalcodeinits[i])
            react(finalcodeinits[i])
                
        cv2.imshow('Binary image',image)
        cv2.waitKey(0)   
        
        
        
                
        
        
        
