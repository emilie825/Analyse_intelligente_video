from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    summary = ""
    filename = ""

    if 'videoFile' in request.files and request.files['videoFile'].filename != '':
        file = request.files['videoFile']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        summary = f"Résumé de la vidéo \"{filename}\" : Cette vidéo a été analysée avec succès."

    elif 'audioFile' in request.files and request.files['audioFile'].filename != '':
        file = request.files['audioFile']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        summary = f"Résumé de l'audio \"{filename}\" : Ce fichier audio a été analysé avec succès."

    elif 'userText' in request.form and request.form['userText'].strip() != '':
        user_text = request.form['userText'].strip()
        summary = f"Résumé du texte : \"{user_text[:100]}...\" (Analyse fictive réalisée)."

    else:
        return redirect(url_for('index'))

    return render_template('index.html', filename=filename, summary=summary)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
