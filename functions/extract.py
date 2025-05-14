from moviepy import VideoFileClip
import os

def extract_audio_from_video(video_path):
    clip = VideoFileClip(video_path)
    audio_path = video_path.replace('.mp4', '.wav')
    clip.audio.write_audiofile(audio_path)
    return audio_path
