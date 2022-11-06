# Auth-movies


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
Все команды, приведенные в данном руководстве, выполняются из корневой директории проекта,
если иное не указано в описании конкретной команды.

!!! note
    В этом разделе описан процесс быстрого запуска проекта в режиме `development`. Более
    подробную информацию о работе с сервисом смотри в разделах данного руководства.

### Настройка переменных окружения
Создай файл `.env` в корне проекта, скопировав шаблон `env.template`.

!!! warning
    Ты можешь ничего не менять в файле `.env`. В этом случае убедись, что у тебя свободны порты, указанные
    в следующих переменных:

    * `APP_PORT`
    * `POSTGRES_PORT`
    * `REDIS_PORT`
    * `JAEGER_TCP_PORT`

Создай файлы `.env` в папках `development` и `production` в каталоге `.envs`, используя
соответствующие шаблоны.

### Запуск проекта
Если у тебя доступно выполнение команд с помощью `make`, то смотри вкладку `Make`. Иначе смотри
команду на вкладке `Native`.

Запустить проект в режиме `development`:
=== "Make"

    <div class="termy">

    ```console
    $ make dev

    ---> 100%
    Creating movies_auth-dev_postgres_1 ... <span style="color: green;">done</span>
    Creating movies_auth-dev_jaeger_1   ... <span style="color: green;">done</span>
    Creating movies_auth-dev_redis_1    ... <span style="color: green;">done</span>
    Creating movies_auth-dev_app_1      ... <span style="color: green;">done</span>
    Creating movies_auth-dev_nginx_1    ... <span style="color: green;">done</span>
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

    ---> 100%
    Creating movies_auth-dev_postgres_1 ... done
    Creating movies_auth-dev_jaeger_1   ... done
    Creating movies_auth-dev_redis_1    ... done
    Creating movies_auth-dev_app_1      ... done
    Creating movies_auth-dev_nginx_1    ... done
    ```

    </div>

??? note "Что делает команда `make dev`"
    Команда `make dev` запускает проект в докере, используя docker-compose.
