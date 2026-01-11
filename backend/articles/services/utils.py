from django.utils import timezone
from django.db.models import QuerySet

from datetime import timedelta
import hashlib
import json

from articles.models import (
    ArticleSnapshot,
    PublishedArticle,
)


def hash_and_normalize(title, content):
    """
    Make a 'stable representation of the article and calculate its hash value (SHA-256)'

    What it does:
     - strip the spaces before and after the title and the summary
    """

    items_to_hash = {
        'title': title.strip(),
        'content': content,
    }
    items_json = json.dumps(items_to_hash, sort_keys=True)

    # noinspection InsecureHash
    return hashlib.sha256(items_json.encode('utf-8')).hexdigest()


def get_last_snapshot(article):
    """
    Return the most recent snapshot of the article
    """
    return (
        ArticleSnapshot.objects
        .filter(article=article)
        .order_by('-created_at')
        .first()
    )


def get_published_version(article):
    """
    Return the published version of the article
    """
    return PublishedArticle.objects.filter(article=article).first()


def within_submit_cooldown(last_moderation_at, hours=24):
    # First time submit
    if not last_moderation_at:
        return False

    now = timezone.now()

    return now - last_moderation_at < timedelta(hours=hours)
