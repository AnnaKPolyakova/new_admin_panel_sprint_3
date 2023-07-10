import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1").split(" ")

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1", "http://51.250.104.105"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCALE_PATHS = ["movies/locale"]

# LOCAL = int(os.environ.get('LOCAL', 0)) == 1

PAGINATION_SIZE = os.environ.get("PAGINATION_SIZE", 50)

SIZE_FOR_LOAD_TO_ELASTICSEARCH = int(
    os.environ.get("SIZE_FOR_LOAD_TO_ELASTICSEARCH", 50)
)

SETTINGS_FOR_CELERY = os.getenv("SETTINGS_FOR_CELERY")


ELASTICSEARCH_HOSTNAME = os.environ.get("ELASTICSEARCH_HOSTNAME", 'localhost')
ELASTICSEARCH_PORT = os.environ.get("ELASTICSEARCH_PORT", 9200)
ELASTICSEARCH_PROTOCOL = os.environ.get("ELASTICSEARCH_PROTOCOL", 'http')
