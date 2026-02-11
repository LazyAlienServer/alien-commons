from django.conf import settings

import requests

from .cache import set_cache


YOUTUBE_API_URL = settings.YOUTUBE_API_URL
YOUTUBE_REQUEST_HEADERS = settings.YOUTUBE_REQUEST_HEADERS


def fetch_youtube_data():
    """Fetch YouTube Data and Update Cache"""

    header, url = YOUTUBE_REQUEST_HEADERS, YOUTUBE_API_URL
    response = requests.get(url, headers=header)
    data = response.json()

    set_cache("youtube_data", "channel_stats", value=data, timeout=None)
