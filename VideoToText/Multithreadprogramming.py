import os
import re
import pandas as pd
import yt_dlp
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
from multiprocessing.dummy import Pool as ThreadPool

def download_video(url_output_path):
    url, output_path = url_output_path
    ydl_opts = {'outtmpl': output_path, 'format': 'best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def extract_audio(video_path_audio_path):
    video_path, audio_path = video_path_audio_path
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
    finally:
        audio.close()
        video.close()

def split_audio(audio_path_chunk_length):
    audio_path, chunk_length_ms = audio_path_chunk_length
    audio = AudioSegment.from_wav(audio_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_name = f"chunk_{i // chunk_length_ms}.wav"
        chunk.export(chunk_name, format="wav")
        chunks.append(chunk_name)
    return chunks

def recognize_audio_chunk(chunk):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(chunk) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(f"Chunk {chunk} processed")
            return text
    except Exception as e:
        print(f"Error processing chunk {chunk}: {e}")
        return ""

def process_video(video_info):
    index, video_url, output_folder, chunk_length_ms = video_info
    try:
        video_path = f"downloaded_video{index}.mp4"
        audio_path = f"audio{index}.wav"

        download_video((video_url, video_path))
        extract_audio((video_path, audio_path))

        chunks = split_audio((audio_path, chunk_length_ms))

        pool = ThreadPool()
        texts = pool.map(recognize_audio_chunk, chunks)
        pool.close()
        pool.join()

        episode_number = re.search(r"episode-(\d+)", video_url).group(1)
        transcript_path = os.path.join(output_folder, f"transcript_{episode_number}.txt")
        
        with open(transcript_path, 'w') as f:
            for text in texts:
                f.write(text + " ")
        
        os.remove(video_path)
        os.remove(audio_path)
        for chunk in chunks:
            os.remove(chunk)
    except Exception as e:
        print("Problem with url:", e)

def process_videos_from_excel(excel_path, output_folder="Bannon", chunk_length_ms=60000):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        df = pd.read_excel(excel_path)
        df = df.dropna()
        print(df.head(5))
    except FileNotFoundError:
        print(f"Error: The file '{excel_path}' does not exist.")
        return

    for index, row in df.iterrows():
        video_info = (index, f"https://rumble.com{row['href']}", output_folder, chunk_length_ms)
        process_video(video_info)

if __name__ == "__main__":
    excel_path = 'bannon2.xlsx'  # Update this path if necessary
    process_videos_from_excel(excel_path)
