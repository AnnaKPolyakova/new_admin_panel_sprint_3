REDIS_HOST = "0.0.0.0:"
REDIS_PORT = "6379"
CELERY_BROKER_URL = "redis://" + REDIS_HOST + REDIS_PORT + "/0"
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + REDIS_PORT + "/0"