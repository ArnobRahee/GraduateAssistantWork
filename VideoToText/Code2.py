import yt_dlp
from pydub import AudioSegment
import speech_recognition as sr
import os

def download_video(url, output_path="downloaded_video.mp4"):
    ydl_opts = {'outtmpl': output_path, 'format': 'bestaudio/best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def convert_to_audio(video_path, chunk_length_ms=60000):
    audio = AudioSegment.from_file(video_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        chunks.append(chunk)
    return chunks

def recognize_audio(audio_chunks):
    recognizer = sr.Recognizer()
    full_transcript = ""  # Initialize an empty string to hold the full transcript
    for i, chunk in enumerate(audio_chunks):
        chunk_path = f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                full_transcript += text + " "  # Append the recognized text to the full transcript
            except sr.UnknownValueError:
                print(f"Chunk {i+1} - Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Chunk {i+1} - Could not request results from Google Speech Recognition service; {e}")
        os.remove(chunk_path)
    print(f"Full Transcript: {full_transcript}")  # Print the full transcript after processing all chunks

if __name__ == "__main__":
    video_url = 'https://hugh.cdn.rumble.cloud/video/s8/2/v/C/6/A/vC6Aq.caa.mp4?u=3'  # Replace with your video URL
    video_path = "downloaded_video.mp4"  # Temporary video file path

    # Download video
    download_video(video_url, video_path)

    # Convert video to audio chunks
    audio_chunks = convert_to_audio(video_path)

    # Perform speech-to-text conversion on each chunk and print the full transcript at the end
    recognize_audio(audio_chunks)

    # Optionally, remove the temporary video file
    os.remove(video_path)
