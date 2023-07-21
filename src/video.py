import os

from googleapiclient.discovery import build


class Video:

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_info = self.get_info()
        self.video_name = self.video_info["items"][0]["snippet"]["title"]
        self.video_link = f'https://www.youtube.com/watch?v={self.video_id}'
        self.video_views = self.video_info["items"][0]["statistics"]["viewCount"]
        self.video_likes = self.video_info["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return self.video_name

    def get_info(self):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_info = youtube.videos().list(id=self.video_id, part='snippet,statistics,contentDetails,topicDetails').execute()
        return video_info


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
