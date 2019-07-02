import requests
import json
import datetime

from collections import OrderedDict

from youtube_project.settings import YOUTUBE_SECRET_KEY


def youtube_search(search_query):
    YOUTUBE_URI = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q={}&key={}'
    FORMAT_YOUTUBE_URI = YOUTUBE_URI.format(search_query, YOUTUBE_SECRET_KEY)

    content = requests.get(FORMAT_YOUTUBE_URI).text
    data = json.loads(content)
    video_list = []
    keys = 'video_id', 'title', 'description', 'preview', 'published'

    for item in data.get('items'):
        video_id = item.get('id').get('videoId')
        title = item.get('snippet').get('title')
        description = item.get('snippet').get('description')
        preview = item.get('snippet').get('thumbnails').get('high').get('url')
        published = datetime.datetime.strptime(item.get('snippet').get('publishedAt'), "%Y-%m-%dT%H:%M:%S.%f%z")

        values = video_id, title, description, preview, published

        if video_id:
            video_item = OrderedDict(zip(keys, values))
            video_list.append(video_item)

    return video_list
