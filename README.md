# Data loader into Elasticsearch from PostgreSQL.

Technologies and requirements:
```
Python 3.9+
Django
```

### Docker Settings

##### Installation

* [Detailed installation guide](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### Docker-compose settings

##### Installation

* [Detailed Installation Guide](https://docs.docker.com/compose/install/)

### Launch the application

#### Before starting the project, create environment variables
Create a .env in the root and add the necessary variables to it
Example for partial running in .env.example-local containers
Example for full run in .env.example-docker containers

#### Running a project entirely in docker containers

* `docker-compose up --build`

#### Commands for running bd in a container + applications locally

* `docker-compose -f docker-compose-local.yml up --build` - create and run docker containers
* `python manage.py runserver --settings config.settings-local` - run
   project
* `celery -A etl worker -l info` - launch worker celery
* `celery -A etl beat -l info` - run beat celery

#### Loading via management

* `python manage.py load_films'
  or
* `python manage.py load_films --settings config.settings-local'
