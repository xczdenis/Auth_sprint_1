# Запуск тестов
Тесты можно запускать в двух режимах: локально и в докере.


## Запустить тесты в докере

Запустить тесты в докере (логи будут выведены в консоли):
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



## Запустить тесты локально

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


## Остановить и удалить запущенные контейнеры тестов
=== "Make"

    <div class="termy">

    ```console
    $ make down
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.test.yml down
    ```

    </div>

