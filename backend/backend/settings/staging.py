from .base import *

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": "5432"
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
        "KEY_PREFIX": "staging",
    }
}

SITE_URL = env.str("SITE_URL")

YOUTUBE_API_KEY = env.str("YOUTUBE_API_KEY")
YOUTUBE_API_URL = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={YOUTUBE_CHANNEL_ID}&key={YOUTUBE_API_KEY}"
