
<h2>Requirements</h2>

- Python 3.7
- OpenCV
- PyTesseract
- Flask

Dependencies for Python could be installed via **pip** after installing Python with your package manager.
A virtual environment is also necessary for Flask, so pip dependencies commands must be executed inside a venv. Paste this line
after venv activation (read below):

```sh
pip3 install opencv-python pytesseract flask
```

<h2>Behaviour</h2>

A webapp made with Flask python framework. It converts a previously uploaded .jpg business card into a JSON parsed file with infos like: name, surname, company and mail.
OpenCV is used for grayscaling and optimize images before PyTesseract processing. The latter lib is used to extract texts with OCR (optical character recognition) technique.
_**bcModules.py**_ also contains functions for shooting pic with a camera module instead of static file uploading, but it's not implemented in webapp yet.



<h2>Running</h2>

Open a shell and cd into project folder with venv and required libs already installed.
To run the Flask webapp you have to activate the virtual environment:

<h3>Linux</h3>

```sh
python3.9 -m venv venv
. venv/bin/activate 
export FLASK_APP=app.py
```

<h3>OSX</h3>

```sh
python3.9 -m venv venv
source venv/bin/activate
export FLASK_APP=app.py
```
  
<h3>Windows</h3>

```batch
py -3 -m venv venv
dir <project_name>
venv\Scripts\activate
setx FLASK_APP "app.py"
```

Then for all OS: 

```
flask run
```

From now webapp will be available @ http://127.0.0.1:5000. Enjoy

