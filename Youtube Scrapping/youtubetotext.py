import os
import pandas as pd
import yt_dlp
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from pytube.exceptions import VideoUnavailable

def get_video_title_pytube(video_id):
    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        return yt.title
    except VideoUnavailable:
        print(f"Video with ID {video_id} is unavailable.")
        return None
    except Exception as e:
        print(f"An error occurred while fetching the title for video ID {video_id} using pytube: {e}")
        return None

def get_video_title_ytdlp(video_id):
    try:
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            'skip_download': True,
            'force_generic_extractor': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            return info_dict.get('title', None)
    except Exception as e:
        print(f"An error occurred while fetching the title for video ID {video_id} using yt-dlp: {e}")
        return None

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for video ID: {video_id}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_transcript(transcript, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in transcript:
            start = entry['start']
            duration = entry['duration']
            text = entry['text']
            file.write(f"[{start:.2f} - {start + duration:.2f}] {text}\n")

if __name__ == "__main__":
    excel_path = 'archive.xlsx'  # Path to the provided Excel file
    output_folder = "Moms 4 Liberty"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Process each video ID
    for index, row in df.iterrows():
        video_id = row['videoid']  # Updated to use the correct column name
        
        # Try to get video title using pytube first
        video_title = get_video_title_pytube(video_id)
        
        # If pytube fails, try yt-dlp
        if not video_title:
            video_title = get_video_title_ytdlp(video_id)
        
        # Use video ID as the filename if title couldn't be fetched
        sanitized_title = video_id if not video_title else "".join(x for x in video_title if (x.isalnum() or x in "._- ")).replace(" ", "_")
        
        # Get transcript
        transcript = get_video_transcript(video_id)

        if transcript:
            file_name = os.path.join(output_folder, f"{sanitized_title}_transcript.txt")
            save_transcript(transcript, file_name)
            print(f"Transcript saved to {file_name}")
        else:
            print(f"Transcript could not be retrieved for video ID: {video_id}")
