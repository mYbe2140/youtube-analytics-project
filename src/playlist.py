import datetime
import os
import isodate

from googleapiclient.discovery import build


class PlayList:

    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.title = self.playlist_info()['items'][0]['snippet']['localized']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails', maxResults=50).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()

    def playlist_info(self):
        playlist_videos = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        return playlist_videos

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        likes = 0
        more_like_video = ""
        for video_id in self.video_ids:
            video_request = self.youtube.videos().list(id=video_id, part='statistics').execute()
            like_count = video_request['items'][0]['statistics']['likeCount']
            if int(like_count) > likes:
                likes = int(like_count)
                more_like_video = f"https://youtu.be/{video_request['items'][0]['id']}"
        return more_like_video
