import subprocess
import json

# Dictionary mapping playlist names to IDs
playlist_name_to_id = {
    'chaos_communication_congress': 'PL23rUNk2HqJErizLGkuZE99CvGsalwAwX',
    'panels': 'PL23rUNk2HqJHA13g1K-N_xzNICaVwAPIp',
    'podcasts_and_interviews': 'PL23rUNk2HqJG5o2bL-ygVUx83UUxc1CiR',
    'presentations': 'PL23rUNk2HqJEvYdwi3ZWBeCDNa1EGaK_L'
}

# For each playlist in the dictionary...
for playlist_name, playlist_id in playlist_name_to_id.items():
    print(f"Playlist: {playlist_name}")

    # The URL of the playlist
    playlist_url = 'https://www.youtube.com/playlist?list=' + playlist_id

    # Use youtube-dl to fetch the JSON metadata for the playlist
    command_output = subprocess.check_output(['youtube-dl', '--no-check-certificate', '-j', '--flat-playlist', playlist_url])

    # Each line of the output will be a separate JSON object, so we split the lines
    video_metadata = command_output.splitlines()

    # For each video in the playlist...
    for video in video_metadata:
        # Parse the JSON for this video
        video_info = json.loads(video)

        # The URL of the video is under the 'url' field
        video_url = 'https://www.youtube.com/watch?v=' + video_info['id']

        # Print the URL
        print(video_url)

    # Print a newline for readability
    print()
