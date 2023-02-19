import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# Upload settings
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = { 'jpg', 'jpeg', 'png' }

app: Flask = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file'))
        else:
            return redirect(url_for('upload_file'))
    
    return render_template('upload_file.html')
