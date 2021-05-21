#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import pytesseract as pytes
from pytesseract import Output
import time,os,re
from re import search
from os import listdir
import getch as g

# OpenCV lib : shooting pic, grayscaling and manipulating them
# PyTesseract lib : extracting text info from pics

##       ##
##LEGENDA##
##       ##

# | # <comment> ( <method_output> : <return type> )

test=open("test.txt","a")

def regexFind(file):
    str=""
    mailPattern = '\S+@\S+'
    namePattern = "([A-Z][a-z]*)([\\s\\\'-][A-Z][a-z]*)*"

    file.seek(0)
    firstLine = file.readline()

    #  ( m(n) : array[] ) -> m(n)[0] full match
    m=re.search(mailPattern,firstLine)
    n=re.findall(namePattern,firstLine)

    str = m[0]

    #new lists
    firstTElem = []
    secondTElem = []

    for a in n:
        firstTElem.append(a[0])
        secondTElem.append(a[1])

    for i in range(len(secondTElem)):
        x = secondTElem[i]
        if(str.find(x)!=-1 and x!=''):
            print(firstTElem[i])
            print(secondTElem[i])
            break

    
    #for i in range(length):
    #    for x,y in n[i]:
    #        print(x,y)

    return m[0],str


def extraction(frameName):
    #numpy array before converting  
    img = cv.imread(frameName+".jpg")
    img = np.array(img,dtype=np.uint8)

    #gray scale conversion ( gray : output img )
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    #noise removal
    blurred = cv.fastNlMeansDenoising(gray,50,7,21)

    #threshold ( tresh: output img )
    #first arg MUST BE a grayscaled img ; second arg : max pixel value
    #third arg : adaptive threshold type (mean or gaussian) ; fourth arg: threshold type (ONLY binary for adaptive)
    #fifth arg: pixel block size ; 0 black 255 white (max value)
    thresh = cv.adaptiveThreshold(blurred,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,17,1.8)

    #histogram equalization -> improve contrast
    histed = cv.equalizeHist(thresh)

    frameNameFinal = frameName+"__thresh"+str(time.time())+".jpg"
    cv.imwrite(frameNameFinal,histed) #save thresholded img
    print("Img saved: %s" %frameNameFinal)

    img = cv.imread(frameNameFinal)
    #dictionary
    d = pytes.image_to_data(img, output_type=Output.DICT)
    print(d.keys())

    file=open("detected.txt","r+")
    file.truncate(0)

    nBoxes = len(d['text'])
    for i in range(nBoxes):
        print(d['text'][i])
        file.write(d['text'][i]+" ") # tutto su una riga
        test.write(d['text'][i]+" ")

    test.write("\n- - - -\n")
    s1,s2=regexFind(file)
    print(s1+"\n")
    print(s2)
    file.close()
    test.close()
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

# capturing video from camera module
#cap = cv.VideoCapture(0)

#setting max resolution for camera module (5MP)
imgwidth = 2592
imgheight = 1944
#cap.set(3,imgwidth)
#cap.set(4,imgheight)

#if not cap.isOpened():
#    print("Camera error...")
#    exit()

while True: 

    print("X -> take a pic \nY -> from file \nZ -> exit\n")
    b = g.getch()
    print("\n")

    if b=='X' or b=='x':

        #clean if full
        if a==10:
            a=0
        
        #capturing frame by frame
        #ret, frame = cap.read()
        frame_name = time.time()

        #ret==true -> frame read correctly  
       # if not ret:
       #    print("Can't receive the frame..\n")
       #     break

        #saving frame
        #img = cv.imwrite(str(frame_name)+".jpg",frame)
        print("Img saved %s\n" %frame_name)

        #extraction part
        
        text=extraction(frame_name)
        #file.write(text+"\n")

        if list[a]!=0:
            os.remove(str(list[a])+".jpg")
 
        list[a] = frame_name    
        a=a+1
        if a==10:
            a=0

    elif b=='Z' or b=='z':
        #releasing capture
        #cap.release()
        #cleaning folder
        cleaning()
        exit()

    elif b=='Y' or b=='y':
        f="img"
        extraction(f+"3")

    else:
        print("Please insert a correct input.\n")
