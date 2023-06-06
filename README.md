# Auth-movies


## 🚪 API сервис авторизации для Онлайн кинотеатра

Auth-movies - это API сервис авторизации, который обеспечивает мощную и безопасную идентификацию и
аутентификацию пользователей. Используя современные стандарты JWT и OAuth2, он предлагает гибкий интерфейс
для интеграции с любыми приложениями или сервисами. С функционалом управления разрешениями, он позволяет
настраивать сложные ролевые модели, обеспечивая точный контроль доступа.

<hr>

💻 **Исходный код**: <a target="_blanc" href="https://github.com/xczdenis/movies_auth">https://github.com/xczdenis/movies_auth</a>

📖 **Документация**: <a target="_blanc" href="https://xczdenis.github.io/movies_auth">https://xczdenis.github.io/movies_auth</a>

📝 **Open API**:  http://127.0.0.1:5001/api/v1/swagger

<hr>


## ✨ Особенности

* 🐍 **Python 3.11+**;
* Асинхронный **Flask**:
    * С помощью библиотеки `gevent` приложение на `Flask` становится асинхронным;
    * `Blueprints` модули для разделения кода;
    * [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) для работы с базой данных;
    * [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate) для миграций;
    * [flask-jwt-extended](https://flask-jwt-extended.readthedocs.io/en/stable/) для управления JWT;
    * [flasgger](https://github.com/flasgger/flasgger) для OpenAPI;
    * [flask-pydantic](https://pypi.org/project/Flask-Pydantic/) для валидации параметров запросов;
    * [flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) для сериализации данных;
* `OAuth2` авторизация;
* Хеширование паролей;
* `PostgreSQL` - основная БД;
* `Redis` - кэш БД, в том числе для хранения отозванных JWT токенов;
* `Jaeger` - распределенная трассировка запросов;
* `Nginx` - proxy-сервер;
* Кастомные [Faker](https://faker.readthedocs.io/en/master/) провайдеры для генерации данных, для полноценного тестирования;
* Полная **Docker** интеграция:
    * тонкие образы - **multi-stage сборка**;
    * **docker-compose** для локальной разработки;
    * тесты в **Docker**;
* [Pre-commit](https://pre-commit.com/) хуки, чтобы код всегда был в отличном состоянии;
* [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) - строгое соблюдение правил написания коммитов;
* **Makefile** для удобного запуска команд;
* **CI/CD**:
    * Telegram оповещение об успешных пулл реквестах;
    * Линтинг;
    * Тесты в докере;
    * Автоматические билдинг документации;
* Удобные **sh** скрипты:
    * [init.sh](https://github.com/xczdenis/movies_auth/blob/main/src/scripts/init.sh) (`make init`) - инициализация проекта;
    * [lint.sh](https://github.com/xczdenis/movies_auth/blob/main/src/scripts/lint.sh) (`make lint`) - линтинг (`black`, `flake8`, `isort`, `autoflake`);
    * [format.sh](https://github.com/xczdenis/movies_auth/blob/main/src/scripts/format.sh) (`make format`) - форматирование;


## 🎨 Функционал сервиса [🔝](#-особенности)

1. Хранение пользователей;
2. Регистрация/вход/выход пользователей;
3. Авторизация по протоколу OAuth2;
4. Аутентификация по JWT;
5. Управление разрешениями;
6. История входов.


## 📚 Requirements [🔝](#-особенности)

Для запуска проекта понадобится:

1. Docker (version ^23.0.5). [Инструкциям по установке](https://docs.docker.com/get-docker/);
2. Docker compose (version ^2.17.3). [Инструкциям по установке](https://docs.docker.com/compose/install/);


## 🚀 Быстрый старт [🔝](#-особенности)

Все команды, приведенные в данном руководстве, выполняются из корневой директории проекта, если иное
не указано в описании конкретной команды.


### 🛠 Настройка переменных окружения  [🔝](#-быстрый-старт-)

Для запуска проекта потребуются переменные окружения, они хранятся в файле `.env`. Создай файл `.env`,
выполнив следующую команду:
```bash
make env
```
Если команды `make` не доступны:
```bash
cp .env.template .env
```
Можно просто создать файл `.env` копированием шаблона `.env.template`.


### 🏁 Запуск проекта [🔝](#-быстрый-старт-)

Запустить проект в докере:
```bash
make run
```

Запустить тесты в докере:
```bash
make tests-docker
```
