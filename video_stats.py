import requests
import json
import os
from datetime import date
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
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e  

# EXTRACT VIDEO DATA
def extract_video_data(video_ids):
    
    extracted_data = []
    
    def batch_list(video_ids, batch_size):
        for video_id in range(0, len(video_ids), batch_size):
            yield video_ids[video_id:video_id + batch_size]
    
    try:
        for batch in batch_list(video_ids, max_result):
            video_id_str = ",".join(batch)
            
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_id_str}&key={API_KEY}"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()   
            
            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
                
                video_data = {
                    "video_id": video_id,
                    "snippet": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get('viewCount', None),
                    "likeCount": statistics.get('likeCount', None),
                    "commentCount": statistics.get('commentCount', None)
                }
                
                extracted_data.append(video_data)
            
        return extracted_data
        
    except requests.exceptions.RequestException as e:
        raise e


# SAVE TO JSON FILE
def save_to_json(extracted_data, file_path):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)
              
              
              
if __name__ == "__main__":
    # Main Data Extraction execution
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
    # Save data to JSON file with current date
    file_path = f"video_data_{date.today()}.json"
    save_to_json(video_data, file_path)