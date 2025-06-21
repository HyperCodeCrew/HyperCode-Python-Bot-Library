import requests
import json

class Youtube:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3/"

    def search(self, query, max_results=10):
        url = f"{self.base_url}search"
        params = {
            "part": "snippet",
            "q": query,
            "key": self.api_key,
            "maxResults": max_results,
            "type": "video"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_video_info(self, video_id):
        url = f"{self.base_url}videos"
        params = {
            "part": "snippet,statistics",
            "id": video_id,
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_channel_info(self, channel_id):
        url = f"{self.base_url}channels"
        params = {
            "part": "snippet,statistics",
            "id": channel_id,
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()