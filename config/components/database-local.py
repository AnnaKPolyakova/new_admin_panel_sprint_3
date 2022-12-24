import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("DB_HOST_LOCAL", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", 5432),
        "OPTIONS": {
            "options": "-c search_path=public,content",
        },
    }
}

sqlite_db_path = os.environ.get("SQLITE_DB_PATH")
