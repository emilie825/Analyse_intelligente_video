from flask import Flask, request, render_template, send_file
import json
from werkzeug.utils import secure_filename
from utils import transcribe_audio, summarize_text, extract_audio_from_video, translate_text
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from urllib.parse import unquote

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
    target_lang = request.form.get('target_lang', 'fr')

    print(f"[DEBUG] Langue sélectionnée : {target_lang}")

    filename = ""
    transcription = ""
    summary = ""
    original_transcription = ""
    original_summary = ""
    segments = []

    if mode == "audio":
        file = request.files.get('audioFile')
        if file and file.filename.endswith(('.wav','.mp3')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            transcription, segments = transcribe_audio(filepath)
            summary = summarize_text(transcription)

    elif mode == "video":
        file = request.files.get('videoFile')
        if file and file.filename.endswith(('.mp4','.mov','.avi')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            audio_file_path = extract_audio_from_video(filepath)
            transcription, segments = transcribe_audio(filepath)
            summary = summarize_text(transcription)

    elif mode == "text":
        text = request.form.get('textInput')
        if text:
            transcription = text
            summary = summarize_text(text)

    original_transcription = transcription
    original_summary = summary

    
    print(f"[DEBUG] Traduction en cours vers : {target_lang}")
    transcription = translate_text(original_transcription, target_lang)
    summary = translate_text(original_summary, target_lang)
    print(f"[DEBUG] Traduction terminée.")

    return render_template('index.html',
                           filename=filename,
                           transcription=transcription,
                           summary=summary,
                           mode=mode,
                           target_lang=target_lang,
                           transcription_text=transcription,
                           summary_text=summary,
                           segments=json.dumps(segments))

@app.route("/download/<type>")
def download_text(type):
    content = request.args.get('text', '')
    content = unquote(content)

    if type == "transcription":
        filename = "transcription.pdf"
        title = "Résultat de transcription"
    elif type == "summary":
        filename = "resume.pdf"
        title = "Résultat du résumé"
    else:
        return "Type invalide", 400

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    title_width = pdf.stringWidth(title, "Helvetica-Bold", 16)
    pdf.drawString((width - title_width) / 2, height - 50, title)
    pdf.line((width - title_width) / 2, height - 55, (width + title_width) / 2, height - 55)

    pdf.setFont("Helvetica", 12)
    y = height - 80

    for line in content.split('\n'):
        for chunk in [line[i:i+100] for i in range(0, len(line), 100)]:
            pdf.drawString(50, y, chunk)
            y -= 15
            if y < 50:
                pdf.showPage()
                y = height - 50
                pdf.setFont("Helvetica", 12)

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
