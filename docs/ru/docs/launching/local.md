# Запуск приложения локально
Ты можешь запустить приложение локально, не используя docker.

!!!warning
    Для запуска приложения локально у тебя должна быть запущена база данных и redis:
    === "Make"

        ```bash
        $ make run s="postgres redis"
        ```

    === "Native"

        ```bash
        $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build postgres redis
        ```

!!! success "Action"
    Для запуска приложения локально требуется установить переменную среды `FLASK_APP`
    в значение `src/movies_auth/main.py`:
    ```bash
    export FLASK_APP=src/movies_auth/main.py
    ```

Выполни миграции:
=== "Make"

    <div class="termy">

    ```console
    $ make db-upgrade

    ---> 100%

     INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
     INFO  [alembic.runtime.migration] Will assume transactional DDL.

    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ python -m flask db upgrade

    ---> 100%

     INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
     INFO  [alembic.runtime.migration] Will assume transactional DDL.

    ```

    </div>

Запусти приложение:
=== "Make"

    <div class="termy">

    ```console
    $ make run-local

    ---> 100%

     <span style="color: red;"><b>WARNING: This is a development server. Do not use it ...</b></span>
      * Running on <span style="color: #00b0ff;">http://localhost:5001</span>
     <span style="color: orange;">Press CTRL+C to quit</span>
      * Restarting with watchdog (fsevents)
      * Debugger is active!
      * Debugger PIN: 132-336-641

    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ python src/movies_auth/main.py

    ---> 100%

     <span style="color: red;"><b>WARNING: This is a development server. Do not use it ...</b></span>
      * Running on <span style="color: #00b0ff;">http://localhost:5001</span>
     <span style="color: orange;">Press CTRL+C to quit</span>
      * Restarting with watchdog (fsevents)
      * Debugger is active!
      * Debugger PIN: 132-336-641

    ```

    </div>
