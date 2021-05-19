#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import pytesseract as pytes
import time,os,re
from os import listdir
import getch as g

# OpenCV lib : shooting pic, grayscaling and manipulating them
# PyTesseract lib : extracting text info from pics

##       ##
##LEGENDA dsa dsa##
##       ##

# | # <comment> ( <method_output> : <return type> )

def extraction(frame_name):
    file = open("detected.txt","a")

    #numpy array before converting  
    img = cv.imread(str(frame_name)+".jpg")
    img = np.array(img,dtype=np.uint8)

    #gray scale conversion ( gray : output img )
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    #noise removal
    #blurred = cv.medianBlur(gray,5)
    #blurred = cv.GaussianBlur(gray,(7,5),0)
    blurred = cv.fastNlMeansDenoising(gray,50,7,21)

    #threshold ( tresh: output img )
    #first arg MUST BE a grayscaled img
    #second arg : max pixel value
    #third arg : adaptive threshold type (mean or gaussian)
    #fourth arg: threshold type (ONLY binary for adaptive)
    #fifth arg: pixel block size 
    #sixth arg: constant subtracted from mean   
    # 0 black 255 white (max value)
    
    thresh = cv.adaptiveThreshold(blurred,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,17,1.8)

    #histogram equalization -> improve contrast
    histed = cv.equalizeHist(thresh)

    cv.imwrite(str(frame_name)+"__thresh"+str(time.time())+".jpg",histed) #save thresholded img

    print("Img saved %s\n" %frame_name)

    verticalKernel = cv.getStructuringElement(cv.MORPH_RECT, (1, np.array(img).shape[1]//150))
    erodedImg = cv.erode(histed, verticalKernel, iterations=5)
    verticalLines = cv.dilate(erodedImg, verticalKernel, iterations=5)

    #procedure#
    ###########

    file.close()
    exit()


# service functions #
def cleaning():
    dirname = ""
    c = input("Are you sure to delete all pics? [ Y/N ] : ")
    if c=='y' or c=='Y':
        test = os.listdir(None)
        for pic in test:
            if pic.endswith(".jpg"):
                os.remove(os.path.join(dirname,pic))
        print("All pics deleted.\n")
    elif c=='n' or c=='N':
        print("Exiting...\n")
        exit()
    else:
        print("Please type a correct input.\n")
        cleaning()

    return

# # #

#counter
a=0
list = [0]*10

#destroy if exists
if os.path.exists("detected.txt"):
    os.remove("detected.txt")

# capturing video from camera module
cap = cv.VideoCapture(0)

#setting max resolution for camera module (5MP)
imgwidth = 2592
imgheight = 1944
cap.set(3,imgwidth)
cap.set(4,imgheight)

if not cap.isOpened():
    print("Camera error...")
    exit()

while True: 

    print("X -> take a pic \nY -> from file \nZ -> exit\n")
    b = g.getch()
    print("\n")

    if b=='X' or b=='x':

        #clean if full
        if a==10:
            a=0
        
        #capturing frame by frame
        ret, frame = cap.read()
        frame_name = time.time()

        #ret==true -> frame read correctly  
        if not ret:
            print("Can't receive the frame..\n")
            break

        #saving frame
        img = cv.imwrite(str(frame_name)+".jpg",frame)
        print("Img saved %s\n" %frame_name)

        #extraction part
        
        text=extraction(frame_name)
        file.write(text+"\n")

        if list[a]!=0:
            os.remove(str(list[a])+".jpg")
 
        list[a] = frame_name    
        a=a+1
        if a==10:
            a=0

    elif b=='Z' or b=='z':
        #releasing capture
        cap.release()
        #cleaning folder
        cleaning()
        exit()

    elif b=='Y' or b=='y':
        file="../img"
        extraction(file)

    else:
        print("Please insert a correct input.\n")
