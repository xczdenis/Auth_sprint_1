# Создание среды разработки

!!!danger "Важно"
    Перед началом разработки, выполни все пункты данного раздела!

## Prerequisites
Для успешного развертывания среды разработки понадобится:

1. Docker (version ^20.10.17). Если у тебя его еще нет, следуй [инструкциям по установке](https://docs.docker.com/get-docker/);
2. Docker-compose (version ^1.29.2). Обратись к официальной документации [для установки](https://docs.docker.com/compose/install/);
3. [Pre-commit](https://pre-commit.com/#install).

Также будет полезным:

1. [Hadolint](https://github.com/hadolint/hadolint) - линтер докер файлов.


## 1. Установить пакет libpq-dev
!!!warning
    Этот пакет нужен для корректной работы `psycopg2`. Без этого пакета `psycopg2` не установится.

```bash
sudo apt update
sudo apt install libpq-dev
```

## 2. Установить Poetry
Подробнее про установку Poetry [здесь](https://python-poetry.org/docs/#installation).

**Linux, macOS, Windows (WSL)**
```bash
curl -sSL https://install.python-poetry.org | python3 - --version 1.2.0rc2
```
!!! warning
    Перезапусти ОС после установки Poetry. Также, после установки, необходимо добавить путь
    к Poetry в свой `PATH`. Как правило, это делается автоматически.
    Подробнее смотри в разделе [Add Poetry to your PATH](https://python-poetry.org/docs/#installation).

**Windows (Powershell)**
```bash
> (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py - --version 1.2.0rc2
or
> pip install poetry==1.2.0rc2
```
!!! warning
    Необходимо добавить путь к Poetry в переменную `PATH`. Затем перезапустить IDE.
    Узнать путь к `poetry` можно так:
    ```bash
    where poetry
    ```

## 3. Проверить, что Poetry установлен корректно
```bash
poetry --version

# Poetry (version 1.2.0rc2)
```

## 4. Создать и активировать виртуальную среду
```bash
poetry shell
```

## 5. Установить зависимости
```bash
poetry install
```

## 6. Установить hadolint (опционально)
```bash
sudo wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v2.10.0/hadolint-Linux-x86_64
sudo chmod +x /bin/hadolint
```
