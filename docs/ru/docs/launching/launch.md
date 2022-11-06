# Запуск проекта
Если у тебя доступно выполнение команд с помощью `make`, то используй команду, приведенную на
вкладке `Make` в примерах. Ты можешь выполнять команды нативно, без `make`.
Для этого используй команду из вкладки `Native`.

Для каждой команды существует 2 префикса: `dev` и `prod` (соответствуют режимам `development`
и `production`). Ниже будут приведены команды, с префиксом `dev` - их также можно запускать с префиксом `prod`.

Проект запускается в docker-compose. Название проекта в docker-compose формируется из переменной
окружения `COMPOSE_PROJECT_NAME` (должна быть в корневом файле `.env`).

!!!note
    Если ты используешь `make`, то при запуске команды с префиксом `dev` к имени проекта будет
    добавлен постфикс `-dev`. Например, если `COMPOSE_PROJECT_NAME == movies_auth`, то сервис
    docker-compose будет называться `movies_auth-dev`. Для тестов сервис будет называться
    `movies_auth-test`. При выполнении команд нативно постфиксы не добавляются.

## Запустить все сервисы
=== "Make"

    <div class="termy">

    ```console
    $ make dev

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

    Creating movies_auth_postgres_1 ... <span style="color: green;">done</span>
    Creating movies_auth_jaeger_1   ... <span style="color: green;">done</span>
    Creating movies_auth_redis_1    ... <span style="color: green;">done</span>
    Creating movies_auth_app_1      ... <span style="color: green;">done</span>
    Creating movies_auth_nginx_1    ... <span style="color: green;">done</span>
    ```

    </div>

## Запустить отдельный сервис
Укажи ключ `s` с названием сервиса, чтобы запустить только 1 сервис:
=== "Make"

    <div class="termy">

    ```console
    $ make dev s=postgres

    Creating movies_auth-dev_postgres_1 ... <span style="color: green;">done</span>
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build postgres

    Creating movies_auth_postgres_1 ... <span style="color: green;">done</span>
    ```

    </div>

Можно запустить несколько определенных сервисов:
=== "Make"

    <div class="termy">

    ```console
    $ make dev s="postgres redis"

    Creating movies_auth-dev_postgres_1 ... <span style="color: green;">done</span>
    Creating movies_auth-dev_redis_1    ... <span style="color: green;">done</span>
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build postgres redis

    Creating movies_auth_postgres_1 ... <span style="color: green;">done</span>
    Creating movies_auth_redis_1    ... <span style="color: green;">done</span>
    ```

    </div>

## Посмотреть логи сервиса
Укажите ключ `s` с названием сервиса, чтобы посмотреть его логи:
=== "Make"

    <div class="termy">

    ```console
    $ make dev-logs s=postgres

    <span style="color: orange;">postgres_1</span>  |
    <span style="color: orange;">postgres_1</span>  | PostgreSQL Database directory appears to contain ...
    <span style="color: orange;">postgres_1</span>  |

    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose logs postgres

    <span style="color: orange;">postgres_1</span>  |
    <span style="color: orange;">postgres_1</span>  | PostgreSQL Database directory appears to contain ...
    <span style="color: orange;">postgres_1</span>  |
    ```

    </div>

## Проверить конфигурацию docker-compose
=== "Make"

    <div class="termy">

    ```console
    $ make dev-check
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml config
    ```

    </div>

## Остановить все сервисы
=== "Make"

    <div class="termy">

    ```console
    $ make dev-stop
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose stop
    ```

    </div>

## Остановить конкретный сервис
=== "Make"

    <div class="termy">

    ```console
    $ make dev-stop s=postgres
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose stop postgres
    ```

    </div>

## Остановить все сервисы и удалить контейнеры для окружения dev
Команда доступна только для `make`:
=== "Make"

    <div class="termy">

    ```console
    $ make dev-down
    ```

    </div>

## Остановить все сервисы и удалить контейнеры для всех окружений
=== "Make"

    <div class="termy">

    ```console
    $ make down
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose down
    ```

    </div>
