from .base import *

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "db",  # Set in docker-compose.yml
        "PORT": "5432",  # Default postgres port
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
        "KEY_PREFIX": "dev",
    }
}

SITE_URL = env.str("SITE_URL")

YOUTUBE_API_KEY = env.str("YOUTUBE_API_KEY")
YOUTUBE_API_URL = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={YOUTUBE_CHANNEL_ID}&key={YOUTUBE_API_KEY}"
