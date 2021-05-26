from flask import Flask, render_template, request, redirect, flash, make_response, url_for
import os
import json
import bcModules

app = Flask(__name__)

UPLOAD_FOLDER = 'pics/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/',methods=['GET','POST'])
def hello():

    if request.method == 'POST':
        return redirect(url_for('upload'))

    return render_template('index.html')

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
            
            path=bcModules.extraction(finalPath)

            fp=open(path,'r')
            fp.seek(0)
            f=fp.read()

            res = make_response(f)
            res.headers['Content-Type'] = 'application/json'

            return res

    return render_template('upload.html')

if __name__ == '__main__':
    app.run()