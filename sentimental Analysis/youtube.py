import os
from dotenv import load_dotenv
import googleapiclient.discovery

#Video ID
def extract_video_id(url):
    parts = url.split('=')[-1].split('/')
    return parts[0]

#fetching YouTube comments
def fetch_youtube_comments(api_key, video_url):
    video_id = extract_video_id(video_url)
    
    # YouTube API client
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100,
            pageToken=next_page_token
        )

        response = request.execute()

        for item in response['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append({'comment': comment_text, 'sentiment': None})  # Initialize sentiment as None

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return comments

load_dotenv()
#print('printed env file=',os.getenv("YOUTUBE_API_KEY"))

api_key = os.getenv('YOUTUBE_API_KEY')
if api_key is None:
    raise ValueError("API key is missing. Please check your .env file.")

# Example YouTube video URL
youtube_url = 'https://www.youtube.com/watch?v=czxvoZ73SME'

# Fetch comments
comments = fetch_youtube_comments(api_key, youtube_url)

# Print the first few comments for verification
for comment in comments[:5]:
    print(comment['comment'])
