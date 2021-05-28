
<h2>Requirements</h2>

- Python 3.9.X
- OpenCV
- PyTesseract
- Flask
- Getch

Dependencies for Python could be installed via **pip** after installing Python with your package manager.
A virtual environment is also necessary for Flask, so pip dependencies commands must be executed inside a venv.
In **_utils/_** folder you could find a Bash script for your Unix like OS.


<h2>Behaviour</h2>

A webapp made with Flask python framework. It converts a .jpg business card into a JSON parsed file with infos like: name, surname, company and mail.
OpenCV is used for grayscaling and optimize images before PyTesseract processing. The latter lib is used to extract texts with OCR technique.

<h2>Running</h2>

Open a shell and cd into project folder with venv and required libs already installed.
To run the Flask webapp you have to activate the virtual environment:

<h3>Linux</h3>

> python3 -m venv venv

> . /venv/bin/activate 

> export FLASK_APP=app.py

> flask run

<h3>OSX</h3>

> python3 -m venv venv

> source venv/bin/activate

> export FLASK_APP=app.py

<h3>Windows</h3>

> py -3 -m venv venv

> dir <project_name>

> venv\Scripts\activate

> setx FLASK_APP "app.py"

Then for all OS:
> flask run

From now webapp will be available @ http://127.0.0.1:5000. Enjoy

