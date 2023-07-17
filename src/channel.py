import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    @property
    def title(self):
        return self.print_info()["items"][0]["snippet"]["title"]

    @property
    def description(self):
        return self.print_info()["items"][0]["snippet"]["description"]

    @property
    def url(self):
        return f'https://www.youtube.com/channel/{self.__channel_id}'

    @property
    def subscriber_count(self):
        return self.print_info()["items"][0]["statistics"]["subscriberCount"]

    @property
    def video_count(self):
        return self.print_info()["items"][0]["statistics"]["videoCount"]

    @property
    def view_count(self):
        return self.print_info()["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey='API_KEY')

    def to_json(self, filename):
        channel_dict = {"id": self.__channel_id,
                        "title": self.title,
                        "description": self.description,
                        "url": self.url,
                        "subscriber_count": self.subscriber_count,
                        "video_count": self.video_count,
                        "view_count": self.view_count
                        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(channel_dict, f, indent=2, ensure_ascii=False)
