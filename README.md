# Auth-movies


## 🚪 API сервис авторизации для <a target="_blanc" href="https://github.com/xczdenis/movies">Онлайн кинотеатра</a>

Auth-movies - это API сервис авторизации, который обеспечивает мощную и безопасную идентификацию и
аутентификацию пользователей. Используя современные стандарты JWT и OAuth2, он предлагает гибкий интерфейс
для интеграции с любыми приложениями или сервисами. С функционалом управления разрешениями, он позволяет
настраивать сложные ролевые модели, обеспечивая точный контроль доступа.

<hr>

💻 **Исходный код**: <a target="_blanc" href="https://github.com/xczdenis/movies_auth">https://github.com/xczdenis/movies_auth</a>

📖 **Документация**: <a target="_blanc" href="https://xczdenis.github.io/movies_auth">https://xczdenis.github.io/movies_auth</a>

📝 **Open API**:  <a href="#api">http://127.0.0.1:5001/api/v1/swagger</a>

<hr>


## ✨ Особенности [🔝](#api)

* 🐍 **Python 3.11+**;
* 🔄 Асинхронный **Flask**:
    * С помощью библиотеки `gevent` приложение на `Flask` становится асинхронным;
    * `Blueprints` модули для разделения кода;
    * [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) для работы с базой данных;
    * [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate) для миграций;
    * [flask-jwt-extended](https://flask-jwt-extended.readthedocs.io/en/stable/) для управления JWT;
    * [flasgger](https://github.com/flasgger/flasgger) для OpenAPI;
    * [flask-pydantic](https://pypi.org/project/Flask-Pydantic/) для валидации параметров запросов;
    * [flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) для сериализации данных;
* 🔐 `OAuth2` авторизация;
* 🔒 Хеширование паролей;
* 🐘 `PostgreSQL` - основная БД;
* 🔴 `Redis` - кэш БД, в том числе для хранения отозванных JWT токенов;
* 🔍 `Jaeger` - распределенная трассировка запросов;
* 🔄 `Nginx` - proxy-сервер;
* 🔧 Кастомные [Faker](https://faker.readthedocs.io/en/master/) провайдеры для генерации данных, для полноценного тестирования;
* 🐳 Полная **Docker** интеграция:
    * тонкие образы - **multi-stage сборка**;
    * **docker-compose** для локальной разработки;
    * тесты в **Docker**;
* ✅ [Pre-commit](https://pre-commit.com/) хуки, чтобы код всегда был в отличном состоянии;
* 📝 [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) - строгое соблюдение правил написания коммитов;
* 🔧 **Makefile** для удобного запуска команд;
* 🔄 **CI/CD**:
    * Telegram оповещение об успешных пулл реквестах;
    * Линтинг;
    * Тесты в докере;
    * Автоматические билдинг документации;
* 🔧 Удобные **sh** скрипты:
    * [init.sh](https://github.com/xczdenis/movies_auth/blob/main/src/scripts/init.sh) (`make init`) - инициализация проекта;
    * [lint.sh](https://github.com/xczdenis/movies_auth/blob/main/src/scripts/lint.sh) (`make lint`) - линтинг (`black`, `flake8`, `isort`, `autoflake`);
    * [format.sh](https://github.com/xczdenis/movies_auth/blob/main/src/scripts/format.sh) (`make format`) - форматирование;


## 🎨 Функционал сервиса [🔝](#api)

1. Хранение пользователей;
2. Регистрация/вход/выход пользователей;
3. Авторизация по протоколу OAuth2;
4. Аутентификация по JWT;
5. Управление разрешениями;
6. История входов.


## 📚 Requirements [🔝](#api)

Для запуска проекта понадобится:

1. Docker (version ^23.0.5). [Инструкциям по установке](https://docs.docker.com/get-docker/);
2. Docker compose (version ^2.17.3). [Инструкциям по установке](https://docs.docker.com/compose/install/);


## 🚀 Быстрый старт  [🔝](#api)

Все команды, приведенные в данном руководстве, выполняются из корневой директории проекта, если иное
не указано в описании конкретной команды.

!!! note
    В этом разделе описан процесс быстрого запуска проекта в докере. Более подробную информацию
    о работе с сервисом смотри в разделах данного руководства.


### 🛠 Настройка переменных окружения  [🔝](#_3)

Если у тебя доступно выполнение команд с помощью `make`, то смотри вкладку `Make`. Иначе смотри
команду на вкладке `Native`.

Для запуска проекта потребуются переменные окружения, они хранятся в файле `.env`. Создай файл `.env`,
выполнив следующую команду:
=== "Make"

    <div class="termy">

    ```console
    $ make env

    File <span style="color: lightgreen;">.env</span> created from <span style="color: lightgreen;">.env.template</span>!
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ cp .env.template .env

    File <span style="color: lightgreen;">.env</span> created from <span style="color: lightgreen;">.env.template</span>!
    ```

    </div>

Можно просто создать файл `.env` копированием шаблона `.env.template`.


### 🏁 Запуск проекта  [🔝](#_3)

Запустить проект в докере:
=== "Make"

    <div class="termy">

    ```console
    $ make run

    ---> 100%

     ✔ Network movies_auth_default       <span style="color: lightgreen;">Created</span>
     ✔ Container movies_auth-redis-1     <span style="color: lightgreen;">Started</span>
     ✔ Container movies_auth-jaeger-1    <span style="color: lightgreen;">Started</span>
     ✔ Container movies_auth-postgres-1  <span style="color: lightgreen;">Healthy</span>
     ✔ Container movies_auth-app-1       <span style="color: lightgreen;">Healthy</span>
     ✔ Container movies_auth-proxy-1     <span style="color: lightgreen;">Started</span>
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

    ---> 100%

     ✔ Network movies_auth_default       <span style="color: lightgreen;">Created</span>
     ✔ Container movies_auth-redis-1     <span style="color: lightgreen;">Started</span>
     ✔ Container movies_auth-jaeger-1    <span style="color: lightgreen;">Started</span>
     ✔ Container movies_auth-postgres-1  <span style="color: lightgreen;">Healthy</span>
     ✔ Container movies_auth-app-1       <span style="color: lightgreen;">Healthy</span>
     ✔ Container movies_auth-proxy-1     <span style="color: lightgreen;">Started</span>
    ```

    </div>

??? note "Что делает команда `make run`"
    Команда `make run` запускает проект в докере, используя docker-compose.


### 🧪 Тесты  [🔝](#_3)

!!! warning "Выполни `make run` перед запуском тестов локально"
    Для локального запуска тестов требуются запущенные контейнеры с базой данных и Redis. Поэтому перед
    локальным запуском тестов, выполни команду `make run`.


Запустить тесты локально:
=== "Make"

    <div class="termy">

    ```console
    $ make tests

    ---> 100%

     ::TestSignin...     <span style="color: green;">PASSED         [  5%]</span>
     ::TestSignup...     <span style="color: green;">PASSED         [ 10%]</span>
     ::TestRefresh...    <span style="color: green;">PASSED         [ 15%]</span>
     ::TestLogout...     <span style="color: green;">PASSED         [ 20%]</span>
     ...
     tests...            <span style="color: green;">PASSED         [100%]</span>

    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ python -m pytest

    ---> 100%

     ::TestSignin...     <span style="color: green;">PASSED         [  5%]</span>
     ::TestSignup...     <span style="color: green;">PASSED         [ 10%]</span>
     ::TestRefresh...    <span style="color: green;">PASSED         [ 15%]</span>
     ::TestLogout...     <span style="color: green;">PASSED         [ 20%]</span>
     ...
     tests...            <span style="color: green;">PASSED         [100%]</span>

    ```

    </div>

Запустить тесты в докере:
=== "Make"

    <div class="termy">

    ```console
    $ make tests-docker

    ---> 100%

     ::TestSignin...     <span style="color: green;">PASSED         [  5%]</span>
     ::TestSignup...     <span style="color: green;">PASSED         [ 10%]</span>
     ::TestRefresh...    <span style="color: green;">PASSED         [ 15%]</span>
     ::TestLogout...     <span style="color: green;">PASSED         [ 20%]</span>
     ...
     tests...            <span style="color: green;">PASSED         [100%]</span>

    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.test.yml --profile default --profile tests build
    $ docker-compose -f docker-compose.yml -f docker-compose.test.yml --profile default --profile tests run tests


    ---> 100%

     ::TestSignin...     <span style="color: green;">PASSED         [  5%]</span>
     ::TestSignup...     <span style="color: green;">PASSED         [ 10%]</span>
     ::TestRefresh...    <span style="color: green;">PASSED         [ 15%]</span>
     ::TestLogout...     <span style="color: green;">PASSED         [ 20%]</span>
     ...
     tests...            <span style="color: green;">PASSED         [100%]</span>

    ```

    </div>
