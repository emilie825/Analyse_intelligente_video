from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from utils import transcribe_audio, summarize_text, extract_audio_from_video
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    mode = request.form.get('mode')
    print("Mode choisi:", mode)  # Imprimer la valeur du mode

    filename = ""
    transcription = ""
    summary = ""

    if mode == "audio":
        file = request.files.get('audioFile')
        if file and file.filename.endswith(('.wav', '.mp3')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Fichier audio reçu: {filename}, Sauvegarde à {filepath}")
            file.save(filepath)
            transcription = transcribe_audio(filepath)
            summary = summarize_text(transcription)

    elif mode == "video":
        file = request.files.get('videoFile')
        if file and file.filename.endswith(('.mp4', '.mov', '.avi')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Fichier vidéo reçu: {filename}, Sauvegarde à {filepath}")
            file.save(filepath)

            # Extraction audio de la vidéo
            audio_file_path = extract_audio_from_video(filepath)
            transcription = transcribe_audio(audio_file_path)
            summary = summarize_text(transcription)

    elif mode == "text":
        text = request.form.get('textInput')
        if text:
            transcription = text
            summary = summarize_text(text)

    return render_template(
        'index.html',
        filename=filename,
        transcription=transcription,
        summary=summary,
        mode=mode
    )


if __name__ == '__main__':
    app.run(debug=True)
