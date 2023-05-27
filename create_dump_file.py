import openai
import os
import subprocess
import json
from urllib.parse import urlparse, parse_qs

# Your OpenAI key
openai_api_key = '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'
openai.api_key = openai_api_key

# Directory to save the MP3 and transcript files
output_dir = './joschabach/outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Custom header and footer
footer = 'YOUR_FOOTER'

header = ('This is a text dump of transcripts generated from a series of YouTube videos featuring the philosopher Joscha Bach. '
          'The aim is to create a comprehensive almanac of his thoughts. Each entry includes the video title, description, '
          'original YouTube URL, and a full transcript, which was transcribed using OpenAI\'s Whisper Automatic Speech Recognition system. '
          'Please note that some transcripts may also contain text from podcast hosts or other speakers interacting with Joscha Bach.')


# Open the file containing the video URLs
with open('joschabach/all_urls_cleaned.txt', 'r') as url_file:
    first_url = True
    # For each URL in the file...
    for url in url_file:
        url = url.strip()  # Remove leading/trailing whitespace

        # Use youtube-dl to fetch the JSON metadata for the video
        command_output = subprocess.check_output(['youtube-dl', '--no-check-certificate', '-j', url])
        video_info = json.loads(command_output)

        # Extract the video title and description
        title = video_info['title']
        description = video_info['description']

        # Download the audio of the video in MP3 format
        audio_filename = os.path.join(output_dir, video_info['id'] + '.mp3')
        subprocess.check_output(['youtube-dl', '--no-check-certificate', '-x', '--audio-format', 'mp3', '-o', audio_filename, url])

        # Transcribe the audio file using Whisper
        with open(audio_filename, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file).alternatives[0].transcript

        # Create a text file for this video
        text_filename = os.path.join(output_dir, video_info['id'] + '.txt')
        with open(text_filename, 'w') as text_file:
            text_file.write(f'Name: {title}\n')
            text_file.write(f'Description: {description}\n')
            text_file.write(f'Youtube URL: {url}\n')
            text_file.write(f'Transcript: {transcript}\n')

        # Append this transcript to the aggregate file
        with open(os.path.join(output_dir, 'aggregate.txt'), 'a') as aggregate_file:
            if first_url:
                first_url = False
                aggregate_file.write(header)
            aggregate_file.write(f'Name: {title}\n')
            aggregate_file.write(f'Description: {description}\n')
            aggregate_file.write(f'Youtube URL: {url}\n')
            aggregate_file.write(f'Transcript: {transcript}\n')

