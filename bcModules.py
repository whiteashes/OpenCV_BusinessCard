import cv2 as cv
import numpy as np
import pytesseract as pytes
from pytesseract import Output
import time,os,re
from re import A, search
from os import listdir
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

def cvProcessing(frameName):
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

    #

    frameNameFinal = frameName+"__thresh"+str(time.time())+".jpg"
    cv.imwrite(frameNameFinal,histed) #save thresholded img
    print("Img saved: %s" %frameNameFinal)

    img = cv.imread(frameNameFinal)

    return img

def callPyTes(img):
    return pytes.image_to_data(img, output_type=Output.DICT,config='--psm 11 -c tessedit_do_invert=0',lang='ita',)


def openAndWrite(d):
    file=open("detected.txt","r+")
    file.truncate(0)

    nBoxes = len(d['text'])
    for i in range(nBoxes):
        file.write(d['text'][i]+" ") # tutto su una riga
    
    return file


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
        "mail": "",
        "website": "",
        "piva": "",
        "phone": ""
    }

    #for more accuracy with names
    titles = ['Dott.','Ing.','Dott.ssa','Avv.']

    file.seek(0)
    firstLine = file.readline()
    print(firstLine)

    #splitting in words
    arr = firstLine.split()

    #finding using titles
    for i in range(len(arr)):

        if re.search("P.IVA",arr[i]) or re.search("P IVA",arr[i]) or re.search("PIVA",arr[i]):
            card['piva'] = arr[i+1]
        
        if re.search("+39",arr[i]):
            if arr[i+1]==" " or len(arr[i+1])<6:
                card['phone'] = "+39"+arr[i+2]
            else:
                card['phone'] = "+39"+arr[i+1]

        if re.search("www",arr[i],re.IGNORECASE) or re.search("https",arr[i],re.IGNORECASE) or re.search("http",arr[i],re.IGNORECASE):
            card['website'] = arr[i]

        for x in range(len(titles)):
            if re.search(titles[x],arr[i]):
                card['name'] = arr[i+1]

                if(len(arr[i+2])<=4):
                    card['surname'] = arr[i+2] + " " + arr[i+3]
                else:
                    card['surname'] = arr[i+2]
            x=x+1
        i=i+1

   
    #  ( m(n) : array[] ) -> m(n)[0] full mat
    try:
        m=re.search(mailPattern,firstLine)
    except TypeError:
        print("Mail not found.")
        exit()

    #mail
    card['mail'] = m[0]
    card['mail'] = card['mail'].replace(':','.')

    #company by mail
    card['company'] = card['mail'].split("@")[1].split(".")[0].capitalize()
    

    #if it did not find name by titles
    if card['name']=="" or card['surname']=="":
        
        #regex matching between name pattern and first line
        n=re.findall(namePattern,firstLine)

        #new lists
        firstTElem = []
        secondTElem = []

        #for loop over name matches
        #splitting dict into two separate arrays
        for a in n:
            if not a[0]=='' or a[0]==' ':
                firstTElem.append(a[0])
            else:
                firstTElem.append('X') 

            if not a[1]=='' or a[1]==' ':
                secondTElem.append(a[1])
            else:
                secondTElem.append('X')

        stringName = card['mail'].split("@")[0]
        i=0
        for x in firstTElem:
            if re.search(x,stringName,re.IGNORECASE) and len(x)>2:
                card['name'] = x.replace(" ","")
                card['surname'] = secondTElem[i].replace(" ","")
            i=i+1

    print(firstTElem)
    print(secondTElem)

    return card

def extraction(frameName):
    #WINDOWS ONLY,keep comment if you use UNIX like OS#
    # pytes.pytesseract.tesseract_cmd = 'C:\path\to\tesseract.exe'
    
    #if not os.path.exists('pics'):
    #    os.makedirs('pics')
    
    print(frameName)

    img=cvProcessing(frameName)

    #dictionary
    d=callPyTes(img)
    print(d.keys())

    file=openAndWrite(d)
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
