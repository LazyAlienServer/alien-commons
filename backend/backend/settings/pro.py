from .base import *

DEBUG = False

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
        "KEY_PREFIX": "pro",
    }
}

REDIS_PASSWORD = env("REDIS_PASSWORD", default="")
CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@redis:6379/0"
CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@redis:6379/1"
