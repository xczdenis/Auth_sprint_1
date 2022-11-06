<h2 align="center">Auth-movies</h2>


Сервис авторизации для [Онлайн кинотеатра](https://github.com/xczdenis/movies)

<hr>

**Исходный код**: [https://github.com/xczdenis/Auth_sprint_1](https://github.com/xczdenis/Auth_sprint_1)

**Документация**: [https://xczdenis.github.io/Auth_sprint_1/](https://xczdenis.github.io/Auth_sprint_1/)

**Open API**: [http://127.0.0.1:5000/api/v1/swagger/](http://127.0.0.1:5000/api/v1/swagger/)
<hr>


## Функционал сервиса
1. Хранение пользователей;
2. Регистрация/вход/выход пользователей;
3. Аутентификация по JWT;
4. Управление разрешениями;
5. История входов.


## Используемые технологии
1. **Flask** - само приложение;
2. **Postgres** - база данных;
3. **Redis** - k-v хранилище (например, хранит отозванные JWT токены);
4. **Nginx** - веб-сервер;
5. **Jaeger** - распределенная трассировка.

Также используется:

1. Миграции для БД: alembic (точнее [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate));
2. Управление JWT: [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/);
3. ORM: [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/);
4. OpenAPI: [Flasgger](https://github.com/flasgger/flasgger)


## Requirements
* Python 3.10+
* Docker 20.10.17+


## Быстрый старт
Здесь описан процесс быстрого запуска проекта в режиме `development`.
Более подробную информацию о работе с сервисом смотри в документации.

### 1. Настройка переменных окружения
Создай файл `.env` в корне проекта, скопировав шаблон `env.template`.

Ты можешь ничего не менять в файле `.env`. В этом случае убедись, что у тебя свободны порты,
указанные в следующих переменных:

* `APP_PORT`
* `POSTGRES_PORT`
* `REDIS_PORT`
* `JAEGER_TCP_PORT`

Создай файлы `.env` в папках `development` и `production` в каталоге `.envs`, используя
соответствующие шаблоны.

### 2. Запуск проекта
Запустить проект с помощью `make` в режиме `development`:
```bash
$ make dev
```
Запустить проект без `make`:
```bash
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

Что делает команда `make dev`: запускает проект в докере, используя docker-compose.
