from transformers import pipeline
from langdetect import detect

# modèle de résumé anglais multilingue
model_name = "facebook/bart-large-cnn"
summarizer = pipeline("summarization", model=model_name)

def summarize_text(text):
    if len(text) < 50:
        return "Texte trop court pour un résumé."
    return summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
