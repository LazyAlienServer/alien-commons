from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import filepath_to_uri
from django.conf import settings

import uuid
from pathlib import Path
from urllib.parse import urljoin


def avatar_upload_to(instance, filename):
    return str(Path("avatars") / str(instance.username) / f"{uuid.uuid4().hex}.webp")


class AvatarStorage(FileSystemStorage):
    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        url = filepath_to_uri(name)
        if url is not None:
            url = url.lstrip("/")

        if name.startswith("default_avatar/"):
            return urljoin(settings.STATIC_URL, url)
        return urljoin(self.base_url, url)


class ProfileManager(BaseUserManager):
    use_in_migrations = True

    # Superuser does not share this logic
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be filled')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('The <is_staff> value of superusers must be True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('The <is_superuser> value of superusers must be True')

        return self.create_user(email, password, **extra_fields)


class Profile(AbstractUser):
    """
    The User model.
    'id' field is explicitly set in this model.
    """
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        blank=True,
        null=True,
        storage=AvatarStorage()
    )
    signature = models.CharField(
        max_length=60,
        blank=True,
        default="This player is somewhat mysterious..."
    )
    is_moderator = models.BooleanField(default=False)
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ProfileManager()

    def __str__(self):
        return self.username
