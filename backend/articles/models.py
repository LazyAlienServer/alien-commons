from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import TimeStampedMixin, UUIDPrimaryKeyMixin, SoftDeleteMixin


User = get_user_model()


class SourceArticle(TimeStampedMixin, UUIDPrimaryKeyMixin, SoftDeleteMixin):
    """
    Model for all articles

    Local fields:
        - author
        - title
        - content
        - last_moderation_at
        - status

    Mixin fields:
        - created_at
        - updated_at
        - id
        - is_deleted
    """

    class ArticleStatus(models.IntegerChoices):
        """
        5 different article status
        """
        DRAFT = 0, "Draft"
        PENDING = 1, "Pending"
        PUBLISHED = 2, "Published"
        REJECTED = 3, "Rejected"
        UNPUBLISHED = 4, "Unpublished"
        DELETED = 5, "Deleted"

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="articles")

    title = models.CharField(max_length=60, db_index=True, default="")
    content = models.JSONField(blank=True, default=dict)

    status = models.IntegerField(choices=ArticleStatus.choices, default=ArticleStatus.DRAFT, db_index=True)

    last_moderation_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return self.title


class PublishedArticle(UUIDPrimaryKeyMixin, TimeStampedMixin):
    """
    Mixin fields:
    - id
    - created_at
    - updated_at
    """

    article = models.OneToOneField(SourceArticle, on_delete=models.CASCADE, related_name="article_published_version")

    title = models.CharField(max_length=60, db_index=True, default="")
    content = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Published version of article {self.article}"


class ArticleSnapshot(UUIDPrimaryKeyMixin):
    """
    Freeze the current version of the article for review and retrospection.

    Mixin fields:
        - id
    """

    class SnapshotStatus(models.IntegerChoices):

        PENDING = 1, "Pending"
        WITHDRAWN = 2, "Withdrawn"
        APPROVED = 3, "Approved"
        REJECTED = 4, "Rejected"

    article = models.ForeignKey(SourceArticle, on_delete=models.CASCADE, related_name="article_snapshots")

    title = models.CharField(max_length=60, db_index=True, default="")
    content = models.JSONField(blank=True, default=dict)
    content_hash = models.CharField(max_length=64, blank=True, default="", db_index=True)

    created_at = models.DateTimeField(default=timezone.now, db_index=True, editable=False)
    moderation_status = models.IntegerField(choices=SnapshotStatus.choices, default=SnapshotStatus.PENDING, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article', 'created_at']),
            models.Index(fields=['moderation_status', 'created_at']),
            models.Index(fields=['article', 'content_hash']),
        ]

    def __str__(self):
        return f"Snapshot of article {self.article_id} created @ {self.created_at}"


class ArticleEvent(UUIDPrimaryKeyMixin):
    """
    Record events related to articles

    Mixin fields:
        - id
    """

    class EventType(models.IntegerChoices):
        """
        6 different event types
        """

        SUBMIT = 1, "Submit"
        WITHDRAW = 2, "Withdraw"
        APPROVE = 3, "Approve"
        REJECT = 4, "Reject"
        UNPUBLISH = 5, "Unpublish"
        DELETE = 6, "Delete"

    article = models.ForeignKey(SourceArticle, on_delete=models.CASCADE, related_name="article_events")
    snapshot = models.ForeignKey(
        ArticleSnapshot, on_delete=models.SET_NULL, null=True, related_name="related_events"
    )

    annotation = models.TextField(null=True, blank=True)

    event_type = models.IntegerField(choices=EventType.choices)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="article_events_actors")

    created_at = models.DateTimeField(default=timezone.now, db_index=True, editable=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article', 'created_at']),
            models.Index(fields=['actor', 'created_at']),
            models.Index(fields=['snapshot', 'created_at']),
            models.Index(fields=['event_type', 'created_at']),
        ]

    def __str__(self):
        return f"Operation {self.get_event_type_display()} by {self.actor_id} on article {self.article_id} @ {self.created_at}"
