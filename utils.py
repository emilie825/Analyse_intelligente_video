import whisper
from transformers import pipeline
from moviepy import VideoFileClip
import os
from argostranslate import translate, package
import requests

# Chargement des modèles
whisper_model = whisper.load_model("base")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def install_local_argos_models():
    """Installe tous les fichiers .argosmodel du dossier local 'argos_models'"""
    model_dir = os.path.join(os.path.dirname(__file__), "argos_models")
    if not os.path.isdir(model_dir):
        print(f"[WARN] Dossier 'argos_models' non trouvé à l'emplacement : {model_dir}")
        return

    for file in os.listdir(model_dir):
        if file.endswith(".argosmodel"):
            model_path = os.path.join(model_dir, file)
            try:
                package.install_from_path(model_path)
                print(f"[✔] Modèle installé : {file}")
            except Exception as e:
                print(f"[✘] Erreur avec {file} : {e}")

def translate_text(text, target_lang):
    # Détecter la langue source (ici, simple : anglais ou français)
    installed_languages = translate.get_installed_languages()
    target_lang_obj = next((lang for lang in installed_languages if lang.code == target_lang), None)

    if not target_lang_obj:
        return text

    # Cas simple : on a le modèle en direct (ex: en → fr)
    for lang in installed_languages:
        try:
            translation = lang.get_translation(target_lang_obj)
            return translation.translate(text)
        except:
            continue

    # Cas indirect : français vers autre langue via anglais
    source_fr = next((lang for lang in installed_languages if lang.code == "fr"), None)
    target_en = next((lang for lang in installed_languages if lang.code == "en"), None)

    if source_fr and target_en and target_lang != "en":
        try:
            # Étape 1 : fr → en
            fr_en = source_fr.get_translation(target_en)
            english_text = fr_en.translate(text)

            # Étape 2 : en → target
            en_target = target_en.get_translation(target_lang_obj)
            return en_target.translate(english_text)
        except:
            pass

    return text


def summarize_text(text):
    if len(text) < 50:
        return "Le texte est trop court pour être résumé."
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summaries = [summarizer(chunk, max_length=120, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)

def extract_audio_from_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = video_path.rsplit('.', 1)[0] + "_audio.wav"
    video.audio.write_audiofile(audio_path)
    if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
        raise ValueError("Fichier audio extrait vide ou absent.")
    return audio_path

def transcribe_audio(audio_path):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Fichier audio non trouvé : {audio_path}")
    if os.path.getsize(audio_path) == 0:
        raise ValueError("Fichier audio vide.")
    
    result = whisper_model.transcribe(audio_path, verbose=False)
    return result["text"], result["segments"]  # ⬅️ retourne aussi les segments horodatés


# Installation automatique à l'import
install_local_argos_models()

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