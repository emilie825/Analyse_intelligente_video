import whisper
from transformers import pipeline
from moviepy import VideoFileClip
import os

whisper_model = whisper.load_model("base")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    if len(text) < 50:
        return "Le texte est trop court pour être résumé."
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summaries = [summarizer(chunk, max_length=120, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)



from moviepy import VideoFileClip

def extract_audio_from_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = video_path.rsplit('.', 1)[0] + "_audio.wav"
    video.audio.write_audiofile(audio_path)

    if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
        raise ValueError("Le fichier audio extrait est vide ou n'a pas pu être généré.")

    return audio_path


import os
def transcribe_audio(audio_path):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Le fichier audio n'a pas été trouvé : {audio_path}")

    if os.path.getsize(audio_path) == 0:
        raise ValueError("Le fichier audio est vide.")

    result = whisper_model.transcribe(audio_path)
    transcription = result["text"]
    language = result.get("language", "unknown")
    return transcription, language

# calculer la durée de la vidéo 

def get_video_duration(video_path):
    clip = VideoFileClip(video_path)
    duration_sec = int(clip.duration)
    minutes = duration_sec // 60
    seconds = duration_sec % 60
    return f"{minutes:02}:{seconds:02}"

from datetime import datetime
from langcodes import Language

def format_summary_as_report(summary, duration="Inconnue", lang_code="en"):


    # Langue complète à partir du code
    try:
        lang_name = Language.get(lang_code).display_name("fr")
        lang_display = lang_name.capitalize()
    except:
        lang_display = "Inconnue"

    date_today = datetime.today().strftime("%Y-%m-%d")
    return f"""Date : {date_today}
Durée : {duration}
Participants : (inconnus)
Langue d’origine : {lang_display}


Objectif de la réunion :
{summary}


Points clés abordés :
{summary}


Décisions prises :
(A compléter)

Actions à mener :
(A compléter)
"""
