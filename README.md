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

### Запуск приложения

#### Перед запуском проекта создаем переменные окружения
Создаем в корне .env и добавляем в него необходимые переменные
Пример для частичного запуска в контейнерах .env.example-local
Пример для полного запуска в контейнерах .env.example-docker

#### Запуск проекта полностью в контейнерах docker

* `docker-compose up --build`

#### Команды для запуска bd в контейнере + приложения локально

* `docker-compose -f docker-compose-local.yml up --build` - создать и запустить контейнеры docker
* `python manage.py runserver --settings config.settings-local` - запускаем 
  проект
* `celery -A etl worker -l info` - запускаем воркер celery
* `celery -A etl beat -l info` - запускаем beat celery
