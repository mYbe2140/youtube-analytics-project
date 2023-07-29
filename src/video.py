import os

from googleapiclient.discovery import build


class VideoIdError(Exception):
    pass


class Video:

    def __init__(self, video_id: str):
        try:
            self.video_id = video_id
            self.video_info = self.get_info()
            self.title = self.video_info["items"][0]["snippet"]["title"]
            self.video_link = f'https://www.youtube.com/watch?v={self.video_id}'
            self.video_views = self.video_info["items"][0]["statistics"]["viewCount"]
            self.like_count = self.video_info["items"][0]["statistics"]["likeCount"]
        except VideoIdError:
            self.video_info = None
            self.title = None
            self.video_link = None
            self.video_views = None
            self.like_count = None
            print("Неверно указан id видео")

    def __str__(self):
        return self.title

    def get_info(self):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_info = youtube.videos().list(id=self.video_id, part='snippet,statistics,contentDetails,topicDetails').execute()
        if len(video_info['items']) == 0:
            raise VideoIdError
        else:
            return video_info


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
