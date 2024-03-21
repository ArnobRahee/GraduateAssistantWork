import os
import yt_dlp
from moviepy.editor import VideoFileClip
import speech_recognition as sr

def download_video(url, output_path="downloaded_video.mp4"):
    ydl_opts = {'outtmpl': output_path, 'format': 'best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def extract_audio(video_path, audio_path="audio.wav"):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    return audio_path

def split_audio(audio_path, chunk_length_ms=60000):
    audio = AudioSegment.from_wav(audio_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        chunk_name = f"chunk{i//chunk_length_ms}.wav"
        chunk.export(chunk_name, format="wav")
        chunks.append(chunk_name)
    return chunks

def recognize_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_sphinx(audio_data)
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service; {e}")
            return ""

if __name__ == "__main__":
    video_url = 'https://hugh.cdn.rumble.cloud/video/s8/2/2/4/3/A/243Aq.caa.mp4?u=3'  # Replace this with the video URL you want to download and convert
    video_path = "downloaded_video.mp4"
    audio_path = "audio.wav"

    # Download video
    download_video(video_url, video_path)

    # Extract audio from video
    extract_audio(video_path, audio_path)

    # Perform speech-to-text conversion
    full_transcript = recognize_audio(audio_path)
    print(full_transcript)

    # Optionally, remove the temporary files
    os.remove(video_path)
    os.remove(audio_path)
