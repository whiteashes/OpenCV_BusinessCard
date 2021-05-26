import cv2 as cv
import numpy as np
import pytesseract as pytes
from pytesseract import Output
import time,os,re
from re import search
from os import listdir
import getch as g
import json

# OpenCV lib : shooting pic, grayscaling and manipulating them
# PyTesseract lib : extracting text info from pics

##       ##
##LEGENDA##
##       ##

# | # <comment> ( <method_output> : <return type> )

#setting max resolution for camera module (5MP)
IMGWIDTH = 2592
IMGHEIGTH = 1944
#counter
a=0
flag=False
list = [0]*10

def capturing(cap):
    #capturing frame by frame
    ret, frame = cap.read()
    frameName = time.time()

    #ret==true -> frame read correctly  
    if not ret:
        print("Can't receive the frame..\n")
        exit()

    #saving frame
    img = cv.imwrite(str(frameName)+".jpg",frame)
    print("Img saved %s\n" %frameName)

    return frameName

#jsoning dicts
def jsoned(card):
    parsed=card['name']+card['surname']+".json"
    with open(parsed,'w') as fp:
        json.dump(card,fp)
    
    return parsed


def regexFind(file):
    mailPattern = '\S+@\S+'
    namePattern = "([A-Z][a-z]*)([\\s\\\'-][A-Z][a-z]*)*"

    card =	{
        "name": "",
        "surname": "",
        "company": "",
        "mail": ""
    }

    file.seek(0)
    firstLine = file.readline()

    #  ( m(n) : array[] ) -> m(n)[0] full match
    try:
        m=re.search(mailPattern,firstLine)
    except TypeError:
        print("Mail not found.")
        exit()


    card['mail'] = m[0]
    card['mail'] = card['mail'].replace(':','.')

    n=re.findall(namePattern,firstLine)

    #new lists
    firstTElem = []
    secondTElem = []

    #for loop over name matches
    for a in n:
        if not a[0]=='' or a[0]==' ':
            firstTElem.append(a[0])
        else:
            firstTElem.append('X')
        if not a[1]=='' or a[1]==' ':
            secondTElem.append(a[1])
        else:
            secondTElem.append('X')

    #compare matches w\ mail
    i=0
    ignoreNext=''
    for x in secondTElem:
        s=x.replace(" ","")
        if re.search(s,m[0],re.IGNORECASE) and len(s)>1:
            card['surname']=s
            card['name']=firstTElem[i]
            ignoreNext=firstTElem[i]
            
        i=i+1

    #finding company name
    for y in firstTElem:
        s=y.replace(" ","")
        if re.search(s,m[0],re.IGNORECASE) and s!=ignoreNext and len(s)>1:
            card['company']=s

    print(firstTElem)
    print(secondTElem)

    return card


def extraction(frameName):
    print(frameName)

    #numpy array before converting  
    img = cv.imread(frameName)
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
    d = pytes.image_to_data(img, output_type=Output.DICT,config='--psm 11')
    print(d.keys())

    file=open("detected.txt","r+")
    file.truncate(0)

    nBoxes = len(d['text'])
    for i in range(nBoxes):
        file.write(d['text'][i]+" ") # tutto su una riga


    card=regexFind(file)
    parsed=jsoned(card)

    print("jsoned %s" %parsed)
    print(card)

    file.close()
    return parsed


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

def cleaningImg(a,frameName):
    if list[a]!=0:
        os.remove(str(list[a])+".jpg")
        list[a] = frameName    
        a=a+1
    return a