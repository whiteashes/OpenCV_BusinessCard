#!/usr/bin/bash

#python
brew install python

#cloning repo
git clone https://github.com/whiteashes/OpenCV_BusinessCard
cd OpenCV_BusinessCard
mkdir pics
touch detected.txt

#installing venv
pip3 install virtualenv
virtualenv venv 

#activating virtual environment
#to do every time we run a terminal
source venv/bin/activate 

#installing libs inside venv
pip3 install opencv-python 
pip3 install pytesseract
pip3 install getch
pip3 install Flask

#every time we run a venv session
export FLASK_APP=app.py

