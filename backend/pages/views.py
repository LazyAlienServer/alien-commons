from django.core.cache import cache

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from datetime import datetime

from core.utils.cache import get_cache


def days_since_start(date="2023-03-17"):
    now = datetime.now()
    delta = now - datetime.strptime(date, "%Y-%m-%d")
    return delta.days


def fetch_youtube_cache():
    """Fetch cached YouTube data"""

    raw_data = get_cache("youtube_data", "channel_stats")

    if not raw_data:
        return None

    items = raw_data.get("items") or []
    if not items:
        return None
    
    data = items[0]

    return data


class YoutubeSnapshotView(APIView):
    """Return YouTube Channel Snapshot"""

    permission_classes = (AllowAny,)

    def get(self, request):

        data = fetch_youtube_cache()

        if data:
            thumbnail_url = data["snippet"]["thumbnails"]["high"]["url"]
            subscriber_count = data["statistics"]["subscriberCount"]
            video_count = data["statistics"]["videoCount"]
            view_count = data["statistics"]["viewCount"]

            return Response({
                "thumbnail_url": thumbnail_url,
                "subscriber_count": subscriber_count,
                "video_count": video_count,
                "view_count": view_count,
                "since": days_since_start(),
            })
        else:
            return Response({"error": "No data found in cache"})
