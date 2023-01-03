from split_settings.tools import include

include(
    "components/base/application_definition.py",
    "components/base/password_validators.py",
    "components/base/internationalization.py",
    "components/base/logging.py",
    "components/base/corsheaders_settings.py",
    "components/base/media_and_static.py",
    "components/base/base.py",
    "components/debug.py",
    "components/database.py",
    "components/redis.py",
)
