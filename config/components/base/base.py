import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1").split(" ")

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCALE_PATHS = ["movies/locale"]

LOCAL = int(os.environ.get('DEBUG', 0)) == 1

PAGINATION_SIZE = os.environ.get("PAGINATION_SIZE", 50)

SIZE_FOR_LOAD_TO_ELASTICSEARCH = os.environ.get(
    "SIZE_FOR_LOAD_TO_ELASTICSEARCH", 50
)

HOSTNAME = 'localhost'

PORT = 8000

PROTOCOL = 'http'