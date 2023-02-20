import os, shutil
from flask import Flask, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

# Upload settings
BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = { 'jpg', 'jpeg', 'png' }

app: Flask = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def fixed_path(path) -> str:
    """ Return fixed path from 'path' """

    return os.path.join(BASEDIR, path)


def allowed_file(filename: str) -> bool:
    """ True if filename has correct extension """

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('upload_file'))
        
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('upload_file'))
        
        if file and allowed_file(file.filename):
            # Create uploads folder if not exists
            if not os.path.exists(fixed_path(app.config['UPLOAD_FOLDER'])):
                os.makedirs(fixed_path(app.config['UPLOAD_FOLDER']))

            filename = secure_filename(file.filename)
            file.save(os.path.join(BASEDIR, app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file'))
        else:
            return redirect(url_for('upload_file'))
    
    return render_template('upload_file.html')


@app.get('/download_uploads')
def download_uploads():
    shutil.make_archive(fixed_path(app.config['UPLOAD_FOLDER']), 'zip', fixed_path(app.config['UPLOAD_FOLDER']))
    return send_file(fixed_path(f'{app.config["UPLOAD_FOLDER"]}.zip'), as_attachment=True)
