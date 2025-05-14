from flask import Flask, request, jsonify, render_template
from functions.extract import extract_audio_from_video
from functions.transcrypt import transcribe_audio
from functions.summarizer import summarize_text
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.mp4'):
        return jsonify({"error": "Upload a valid .mp4 video file."}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    audio_path = extract_audio_from_video(filepath)
    transcription = transcribe_audio(audio_path)
    summary = summarize_text(transcription)

    return jsonify({
        "audio_path": audio_path,
        "transcription": transcription,
        "summary": summary
    })


@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.wav'):
        return jsonify({"error": "Upload a valid .wav audio file."}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    transcription = transcribe_audio(filepath)
    summary = summarize_text(transcription)

    return jsonify({
        "transcription": transcription,
        "summary": summary
    })


@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided."}), 400

    summary = summarize_text(text)
    
    return jsonify({"summary": summary})


if __name__ == '__main__':
    app.run(debug=True)
