import openai
import os
import yt_dlp
from pydub import AudioSegment
import threading
import json
from datetime import datetime
from dotenv import load_dotenv
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

# Your OpenAI key
openai_api_key = os.environ.get('OPENAI_API_KEY')
print(f"OpenAI API Key: {openai_api_key}")
openai.api_key = openai_api_key

# Directory to save the MP3 and transcript files
output_dir = './joschabach/outputs_multithreaded'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f'Created directory {output_dir}')


import uuid

# Function to process each URL
def process_url(url):
    # Create a YoutubeDL object.
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),  # added filename pattern
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '64',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # Extract the video title, description, and upload date
        title = info.get('title', None)
        description = info.get('description', None)
        upload_date = info.get('upload_date', None)

        # Convert upload_date from 'YYYYMMDD' to a datetime object
        upload_date = datetime.strptime(upload_date, '%Y%m%d')


        # The ID of the video
        video_id = info.get('id', None)

        json_filename = os.path.join(output_dir, f'{video_id}.json')
        # if the json file already exists, skip the video
        if os.path.exists(json_filename):
            print(f'Transcript for {url} already exists. Skipping...')
            return

        print(f'Downloading {url}')

        ydl.download([url])

        # Transcribe the audio file using Whisper
        audio_filename = os.path.join(output_dir, f'{video_id}.mp3')
        print(f'Audio filename: {audio_filename}')
        audio = AudioSegment.from_file(audio_filename)

        # Split audio into chunks of 24.5MB each
        duration_millis = 1000000  # around 24.5 MB
        chunk_length = len(audio) // duration_millis + 1
        print(f'Chunk length: {chunk_length}')
        print(f'Type of Chunk Length: {type(chunk_length)}')
        chunk_length = int(chunk_length)
        chunks = [audio[i*duration_millis:(i+1)*duration_millis] for i in range(chunk_length)]

        transcripts = []
        uuid_str = str(uuid.uuid4())
        for i, chunk in enumerate(chunks):
            # Save chunk to temporary file and transcribe
            chunk_file_name = f"chunk_{uuid_str}_{i}.mp3"
            chunk.export(chunk_file_name, format="mp3")
            with open(chunk_file_name, 'rb') as chunk_file:
                transcript = openai.Audio.transcribe("whisper-1", chunk_file)
                transcripts.append(transcript.text)
            # remove the temporary chunk file after getting the transcript
            os.remove(chunk_file_name)

        # concatenate the transcripts from the chunks to form the complete transcript
        transcript = ' '.join(transcripts)

        # Create a json file for this video
        with open(json_filename, 'w') as json_file:
            json.dump({
                "name": title,
                "id": video_id,
                "url": url,
                "transcript": transcript,
                "description": description,
                "timestamp": upload_date.strftime("%Y-%m-%dT%H:%M:%S")
            }, json_file)

# Define the maximum number of threads to run concurrently
MAX_WORKERS = 5

# Open the file containing the video URLs
with open('joschabach/all_urls.txt', 'r') as url_file:
    urls = url_file.read().splitlines()

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {}
    # For each URL in the file...
    count = 0
    LIMIT = 10
    for url in urls:
        url = url.strip()  # Remove leading/trailing whitespace

        # Check if it already exists in the output directory
        video_id = url.split('=')[1]
        json_filename = os.path.join(output_dir, f'{video_id}.json')
        if os.path.exists(json_filename):
            print(f'Transcript for {url} already exists. Skipping...')
            continue
        
        count += 1
        if count > LIMIT:
            break
        
        # Submit tasks to the executor
        futures[executor.submit(process_url, url)] = url

    # Wait for all tasks to complete
    for future in concurrent.futures.as_completed(futures):
        url = futures[future]
        try:
            print("About to get data")
            data = future.result()
            # write the output json file
            print(f'Writing output for {url}')
            with open(os.path.join(output_dir, f'{data["id"]}.json'), 'w') as f:
                print("Writing to file")
                json.dump(data, f)
        except Exception as e:
            print(f'An error occurred with {url}: {e}')