import os

base_path = './joschabach/'

all_urls = []
podcast_urls = []

with open(os.path.join(base_path, 'all_urls.txt'), 'r') as f:
    all_urls = f.readlines()

with open(os.path.join(base_path, 'podcast_urls.txt'), 'r') as f:
    podcast_urls = f.readlines()

# Remove the newline characters from the end of each line
all_urls = [url.strip() for url in all_urls]
podcast_urls = [url.strip() for url in podcast_urls]

# Find all of the unique URLs
urls_to_download = set(podcast_urls).union(set(all_urls))

# Print the URLs
for url in urls_to_download:
    print(url)



