# Загрузчик данных в Elasticsearch из PostgreSQL.

Технологии и требования:
```
Python 3.9+
Django
```

### Настройки Docker

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### Настройки Docker-compose

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/compose/install/)

#### Перед запуском проекта создаем переменные окружения
Создаем в корне .env и добавляем в него необходимые переменные (пример в .
env.example)

SETTINGS_FOR_CELERY указываем следующие:
* "config.settings" - для запуска всего проекта в контейнерах
* "config.settings-local" - для локальной разработки

## Запуск проекта полностью в контейнерах docker

* `docker-compose up --build`

#### Команды для запуска bd в контейнере + приложения локально

* `docker-compose -f docker-compose-local.yml up --build` - создать и запустить контейнеры docker
* `python manage.py runserver --settings config.settings-local` - запускаем 
  проект
* `celery -A logs worker -l info` - запускаем воркер celery
* `celery -A logs bear -l info` - запускаем beat celery
