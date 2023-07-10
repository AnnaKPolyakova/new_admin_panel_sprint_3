import os

CELERY_CACHE_BACKEND = 'default'
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timoit": 3600}
CELERY_TIMEZONE = "Europe/Moscow"

REDIS_HOST = os.environ.get('REDIS_HOST_LOCAL', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT_LOCAL', '6379')
CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
