from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuration de l'application
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'sh'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assure que le répertoire d'upload existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
        else:
            return 'File type not allowed', 400
    files_list = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files_list)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        return redirect(url_for('index'))
    else:
        abort(404)  # Fichier non trouvé

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=False)
 
