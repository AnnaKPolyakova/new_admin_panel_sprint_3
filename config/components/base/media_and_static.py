
import os

from config.components.base.base import BASE_DIR
from config.components.debug import DEBUG


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


STATIC_URL = "/static/"
if DEBUG is False:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static/"),)

