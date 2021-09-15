from typing import NamedTuple
from cv2 import namedWindow
from flask import Flask, render_template, session, request, redirect, flash, make_response, url_for
import os
import json
import bcModules
import requests
import urllib.request

app = Flask(__name__)

UPLOAD_FOLDER = 'pics/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/',methods=['GET','POST'])
def hello():

    if request.method == 'POST':
        return redirect(url_for('upload'))

    return render_template('index.html')


@app.route('/welcome',methods=['GET','POST'])
def welcome(msg=None):

    if request.method == 'POST':
        return redirect(url_for('hello'))

    return render_template('welcome.html'), {"Refresh":"1; url=/"}


@app.route('/upload',methods=['GET','POST'])
def upload():

    if request.method == 'POST':

        file = request.files['file']

        if file.filename == '':
            return redirect(url_for('upload'))

        if file:
            filename = file.filename
            finalPath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(finalPath)
            
            #json parsed file+namefile
            body,name=bcModules.extraction(finalPath)

            fp=open(name,'r')
            fp.seek(0)
            f=fp.read()

            #1st POST to localhost
            res = make_response(f)
            res.headers['Content-Type'] = 'application/json'

            print(body)
            print(name)

            #2nd POST to server
            url = "http://192.168.46.70:7478/aec/api/MesExecute"
            req = urllib.request.Request(url)
            req.add_header('Content-Type','application/json; charset=utf-8')
            jsondata = json.dumps(body)
            jsonbytes = jsondata.encode('utf-8')

            req.add_header('Authorization','Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqZXRzb24iLCJzaG9ydEV4cCI6MTc4OTE5OTA0MH0.lD5ELumFc6LXyfb7A7FFqTYdgBxivIGO17zDWe5E1nHh-XQEuKrwPCsOAIEK4oEcYYuXRFUBy9TtMH27RrRciw')

            response = urllib.request.urlopen(req,jsonbytes)
            print("Status code: %s" %response.getcode())

            return redirect(url_for('welcome'))


    return render_template('upload.html')

if __name__ == '__main__':
    app.run()