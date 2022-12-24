#!/bin/bash

python manage.py migrate
python manage.py compilemessages -l en -l ru
python manage.py collectstatic --no-input
gunicorn config.wsgi:application --bind 0.0.0.0:8000