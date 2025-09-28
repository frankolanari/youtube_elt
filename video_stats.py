import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"

#GET PLAYLIST ID
def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # print(json.dumps(data, indent = 4)) 
        channel_items = data['items'][0]
        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        #print(channel_playlist_id)
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e

        
# GET VIDEO IDS   
max_result = 50
# base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&key={API_KEY}&playlistId={playlist_id}&maxResults={max_result}"

def get_video_ids(playlist_id):
    print(f"Starting get_video_ids with playlist_id: {playlist_id}")
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&key={API_KEY}&playlistId={playlist_id}&maxResults={max_result}"
    video_ids = []
    page_token = None
    
    try:
        while True:
            url = base_url
            if page_token:
                url += f"&pageToken={page_token}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            page_token = data.get('nextPageToken')
            if not page_token:
                break
        print(f"About to return video_ids: {video_ids}")
        print(f"Length of video_ids: {len(video_ids)}")
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e  


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    print(video_ids)
