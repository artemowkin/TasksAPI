# Tasks List API

Простенькое REST API для менеджера задач

## Prerequisites

Чтобы запустить этот проект, вам нужно иметь:

* `docker`
* `docker-compose`

## Installing

Для начала создаем Docker image

```
$ docker-compose build
```

После этого запускаем созданный образ

```
$ docker-compose up -d
```

Применяем миграции к базе данных

```
$ docker-compose run web python manage.py migrate
```

После этого API будет доступна http://127.0.0.1:8000/

## Authors

* **Artemowkin** - https://github.com/artemowkin/
