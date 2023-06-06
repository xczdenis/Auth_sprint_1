# Запуск проекта

Если у тебя доступно выполнение команд с помощью `make`, то используй команду, приведенную на
вкладке `Make` в примерах. Ты можешь выполнять команды нативно, без `make`. Для этого используй команду
из вкладки `Native`.

Проект запускается в docker-compose. Название проекта в docker-compose формируется из переменной
окружения `COMPOSE_PROJECT_NAME` (должна быть в корневом файле `.env`).


## Запустить все сервисы

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


## Запустить отдельный сервис

Укажи ключ `s` с названием сервиса, чтобы запустить только 1 сервис:
=== "Make"

    <div class="termy">

    ```console
    $ make run s=postgres

    ✔ Container movies_auth-postgres-1  <span style="color: lightgreen;">Started</span>
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build postgres

    ✔ Container movies_auth-postgres-1  <span style="color: lightgreen;">Started</span>
    ```

    </div>

Можно запустить несколько определенных сервисов:
=== "Make"

    <div class="termy">

    ```console
    $ make dev s="postgres redis"

    ✔ Container movies_auth-postgres-1  <span style="color: lightgreen;">Started</span>
    ✔ Container movies_auth-redis-1     <span style="color: lightgreen;">Started</span>
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build postgres redis

    ✔ Container movies_auth-postgres-1  <span style="color: lightgreen;">Started</span>
    ✔ Container movies_auth-redis-1     <span style="color: lightgreen;">Started</span>
    ```

    </div>


## Посмотреть логи сервиса

=== "Make"

    <div class="termy">

    ```console
    $ make logs
    $ Container name: postgres

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
    $ make config
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
    $ make stop
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
    $ make stop
    $ Containers name (press Enter to stop all containers): postgres
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose stop postgres
    ```

    </div>


## Остановить все сервисы и удалить контейнеры

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
