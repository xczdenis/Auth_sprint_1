<h2 align="center">Для Yandex-practicum</h2>
Ссылка на репозиторий: [Auth_sprint_1](https://github.com/xczdenis/Auth_sprint_1)
Исправление замечаний по ревью 1: [PR #1](https://github.com/xczdenis/Auth_sprint_1/pull/1)


<h2 align="center">Auth-movies</h2>


Сервис авторизации для [Онлайн кинотеатра](https://github.com/xczdenis/movies)

Функционал:
1. Хранение пользователей;
2. Регистрация/вход/выход пользователей;
3. Аутентификация по JWT;
4. Управление разрешениями.

Стек (название сервиса - технология):
1. app - само приложение на Flask;
2. postgres - база данных;
3. redis - хранилище отозванных JWT токенов;
4. nginx - веб-сервер.

Также используется:
1. Миграции для БД: alembic (точнее [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate));
2. Управление JWT: [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/);
3. ORM: [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/);
4. OpenAPI: [Flasgger](https://github.com/flasgger/flasgger)


<h2 align="center">Содержание</h2>


1. [Запуск проекта](#запуск-проекта)
   1. [Настройка переменных окружения](#настройка-переменных-окружения)
   2. [Запуск проекта с помощью make](#запуск-проекта-с-помощью-make)
   3. [Запуск тестов](#запуск-тестов)
   4. [Подробнее про Docker](#подробнее-про-docker)
   5. [Запуск проекта без make](#запуск-проекта-без-make)
   6. [Запуск приложения локально](#запуск-приложения-локально)
2. [Режим разработки](#режим-разработки)
   1. [Prerequisites](#prerequisites)
   2. [Создание среды разработки](#создание-среды-разработки)
   3. [Установка pre-commit хуков](#установка-pre-commit-хуков)
3. [Особенности разработки](#особенности-разработки)
   1. [Управление миграциями базы данных](#управление-миграциями-базы-данных)
   2. [Управление зависимостями](#управление-зависимостями)
   3. [Импорты](#импорты)
   4. [Conventional Commits](#conventional-commits)
   5. [Настройки IDE](#настройки-ide)
   6. [Форматер и линтер](#форматер-и-линтер)
4. [Flow работы с проектом](#flow-работы-с-проектом)


<h2 align="center">Запуск проекта</h2>


Все команды, приведенные в данном руководстве, выполняются из корневой директории проекта.


### Настройка переменных окружения
Первое, что нужно сделать, после того как вы создали форк репозитория - настроить переменные окружения.
Для этого нужно создать файлы `.env`.
Для каждого файла `.env` имеется свой файл `.env.template`.

#### Локальные переменные окружения
Создайте файл `.env` в корне проекта - здесь хранятся локальные переменные окружения.
Локальные переменные окружения - это переменные хоста, они используются для запуска с помощью
docker-compose. Здесь хранятся переменные, которые используются на этапе сборки docker-compose,
а не внутри контейнера. Например, здесь вы можете указать порт базы данных, который будет смотреть
наружу. Например, для postgres вы можете указать любой порт отличный от 5432, если он у вас уже занят.

#### Переменные окружения в папке .envs
Папка `.envs` содержит файлы `.env` со всеми переменными окружения, которые используются в проекте.
В отличие от локальных переменных, переменные в папке `.envs` используются внутри контейнера.
Например, здесь порт для postgres должен быть 5432, вне зависимости от того, какой порт указан в
корневом файле `.env`.
Здесь есть 2 каталога:
* development - переменные окружения для запуска в режиме разработки;
* production - переменные окружения для запуска в production режиме.

Создайте файлы `.env` в каждом каталоге.


### Запуск проекта с помощью make
Если вы работаете на Linux и у вас доступно выполнение команд с помощью `make`,
то вы можете использовать команды, приведенные в этом разделе. К сожалению, на Windows
эти команды работать не будут.

*Примечание:* для каждой команды существует 2 префикса: `dev` и `prod` (соответствуют режимам `development`
и `production`). Ниже будут приведены команды, с префиксом `dev` - их также можно запускать с префиксом `prod`.

*Обратите внимание:* docker-compose формирует название проекта из переменной окружения `COMPOSE_PROJECT_NAME`
(должна быть в файле `.env` в корне проекта). При запуске команды с префиксом `dev` к имени проекта
будет добавлено `-dev`. Например, если `COMPOSE_PROJECT_NAME == movies`, то сервис docker-compose
будет называться `movies-dev`. Для тестов сервис будет называться `movies-test`.


#### Запустить все сервисы
```bash
make dev

# make prod - run in production mode
```

#### Запустить конкретный сервис
Укажите ключ `s` с названием сервиса, чтобы запустить только 1 сервис:
```bash
make dev s=postgres
```

#### Посмотреть логи сервиса
Укажите ключ `s` с названием сервиса, чтобы посмотреть его логи:
```bash
make dev-logs s=postgres
```

#### Проверить конфигурацию docker-compose
```bash
make dev-check
```

#### Остановить все сервисы
```bash
make dev-stop
```

#### Остановить конкретный сервис
```bash
make dev-stop s=postgres
```

#### Остановить все сервисы и удалить контейнеры
```bash
make dev-down
```

#### Остановить все сервисы и удалить контейнеры для всех окружений
```bash
make down
```


### Запуск тестов
Тесты можно запускать в двух режимах: интерактивно и в режиме демона.
Запускать тесты в режиме демона удобно для отладки: вы можете подключить сервис Docker в PyCharm,
запустить тесты, изменить код теста и перезапустить контейнер с тестами,
с помощью PyCharm (кнопка Start справа вверху) - это не затронет ваш терминал и не нужно будет выполнять лишние команды:
![test-container-in-pycharm](docs/assets/img/PyCharm/test-container-in-pycharm.png)

Запустить тесты в режиме демона:
```bash
make test
```
Посмотреть логи тестов:
```bash
make test-logs s=tests_app
```
Запустить тесты интерактивно (логи будут в терминале):
```bash
make test-it
```
Остановить запущенные контейнеры тестов:
```bash
make test-stop
```
Остановить и удалить запущенные контейнеры тестов:
```bash
make test-down
```
Проверить конфигурацию тестов:
```bash
make test-check
```


### Подробнее про Docker
Запуск проекта выполняется с помощью docker-compose. Проект содержит следующие файлы docker-compose:
* **docker-compose.yml** - главный файл;
* **docker-compose.dev.yml** - содержит **только изменения** относительно главного файла, необходимые для режима разработки;
* **docker-compose.test.yml** - содержит **только изменения** для запуска тестов;
* **docker-compose.test.dev.yml** - содержит **только изменения** относительно `docker-compose.test.yml`;
* **docker-compose.prod.yml** - содержит **только изменения** для режима `production`;

#### Описание docker-compose.yml
Файл `docker-compose.yml` - это главный compose-файл. Любая команда `docker-compose` должна использовать этот файл в качестве первого аргумента.
Файл содержит все сервисы проекта (кроме тестовых) и основные метаданные для каждого сервиса,
такие как `build`, `env_file`, `depends_on` и т.п.

Файл `docker-compose.yml` **не должен** содержать разделов с монтированием томов (`volume`)
и указанием портов (`ports`), особенно здесь не должно быть портов, смотрящих наружу.

#### Описание docker-compose.dev.yml
Файл `docker-compose.dev.yml` используется для запуска проекта в режиме разработки.
Здесь добавляются изменения относительно `docker-compose.yml`.
Например, здесь можно примонтировать тома для папок приложения и указать порты, смотрящие наружу,
чтобы облегчить отладку.

#### Описание docker-compose.test.yml
Файл `docker-compose.test.yml` содержит сервисы только для тестов. Этого файла достаточно,
чтобы запустить тесты.

Этот файл **не должен** содержать разделов с монтированием томов (`volume`)
и указанием портов (`ports`) из соображений безопасности.
С помощью этого файла запускаются тесты в CI (git hub actions). Несмотря на то,
что тесты запускаются в изолированном контейнере, монтировать папки приложений
при запуске в любой среде, отличной от локального компьютера - это не хорошо.

Вы можете запустить тесты следующей командой:
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d --build
```
При этом не будет выполнено монтирование папок приложений в контейнеры.
Возможно, вы захотите это сделать, чтобы ускорить отладку тестов.
Для этого используется файл `docker-compose.test.dev.yml`.

#### Описание docker-compose.test.dev.yml
Файл `docker-compose.test.dev.yml` используется для запуска тестов в режиме разработки.
Здесь добавляются изменения относительно `docker-compose.test.yml`.
Например, здесь можно примонтировать тома для папок приложения и указать порты, смотрящие наружу,
чтобы облегчить написание и отладку тестов.


### Запуск проекта без make
Запуск в режиме production:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```
Запуск в режиме development:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```
Запуск тестов в режиме production (без монтирования папок приложений):
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d --build
```
Запуск тестов в режиме development (с монтирования папок приложений и открытием портов):
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml -f docker-compose.test.dev.yml up -d --build
```
Для запуска тестов интерактивно, нужно сначала сбилдить образы, а затем запустить контейнер с тестами.

Сбилдить образы:
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml build
```
Запустить тесты:
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml run tests_app
```


### Запуск приложения локально
Вы можете запустить приложение локально, не используя docker.

**Важно:** для запуска приложения локально у вас должна быть запущена база данных и redis:
```bash
make dev s="redis postgres"
or
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build redis postgres
```
**Важно:** установите переменную среды `FLASK_APP` в значение `manage.py`:
```bash
export FLASK_APP=manage.py
```
Теперь вы можете запустить приложение локально. Для этого перейдите в каталог `src`:
```bash
cd src
```
Выполните миграции:
```bash
python -m flask db upgrade
```
Запустите приложение:
```bash
python manage.py
```


<h2 align="center">Режим разработки</h2>


**Важно:** перед началом разработки, выполните все пункты данного раздела!


### Prerequisites
Для успешного развертывания среды разработки вам понадобится:
1. Docker (version ^20.10.17). Если у вас его еще нет, следуйте [инструкциям по установке](https://docs.docker.com/get-docker/);
2. Docker-compose (version ^1.29.2). Обратитесь к официальной документации [для установки](https://docs.docker.com/compose/install/);
3. [Pre-commit](https://pre-commit.com/#install).

Также будет полезным:
1. [Hadolint](https://github.com/hadolint/hadolint) - линтер докер файлов.


### Создание среды разработки
#### 1. Установить пакет libpq-dev
**Важно:** этот пакет нужен для корректной работы `psycopg2`. Без этого пакета `psycopg2` не установится.
```bash
sudo apt update
sudo apt install libpq-dev
```

#### 2. Установить Poetry
Подробнее про установку Poetry [здесь](https://python-poetry.org/docs/#installation).

**Linux, macOS, Windows (WSL)**
```bash
curl -sSL https://install.python-poetry.org | python3 - --version 1.2.0rc2
```
**Важно:** перезапустите ОС после установки Poetry. Также, после установки, необходимо добавить путь к Poetry в свой PATH. Как правило, это делается автоматически.
Подробнее смотри в разделе [Add Poetry to your PATH](https://python-poetry.org/docs/#installation).

**Windows (Powershell)**
```bash
> (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py - --version 1.2.0rc2
or
> pip install poetry==1.2.0rc2
```
**Важно:** необходимо добавить путь к Poetry в переменную `PATH`. Затем перезапустить IDE. Узнать путь к `poetry` можно так:
```bash
where poetry
```

#### 3. Проверить, что Poetry установлен корректно
```bash
poetry --version

# Poetry (version 1.2.0rc2)
```

#### 4. Создать и активировать виртуальную среду
```bash
poetry shell
```

#### 5. Установить зависимости
```bash
poetry install
```

#### 6. Установить hadolint (опционально)
```bash
sudo wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v2.10.0/hadolint-Linux-x86_64
sudo chmod +x /bin/hadolint
```


### Установка pre-commit хуков
#### 1. Проверка установки pre-commit
Пакет [pre-commit](https://pre-commit.com/) включен в список зависимостей и устанавливается командой `poetry install`. Для проверки корректности установки `pre-commit` нужно выполнить команду:
```bash
pre-commit --version
```
В ответ вы должны получить версию pre-commit - это значит, что все установлено корректно:
```bash
pre-commit 2.20.0
```

#### 2. Установка скриптов git hook
```bash
pre-commit install
pre-commit install --hook-type commit-msg
```
Если установка прошла успешно, то увидите следующее сообщение:
```bash
pre-commit installed at .git/hooks/pre-commit
```


<h2 align="center">Особенности разработки</h2>


При разработке необходимо придерживаться установленных правил оформления кода.
В этом разделе вы найдете описание настроек редактора кода, линтеры и форматеры, используемые в проекте,
а также другие особенности, которые необходимо учитывать при разработке.


### Управление миграциями базы данных
После изменения моделей в файле `models.py` нужно сформировать миграции. Перед этим убедитесь,
что у вас запущена база данных. Для выполнения миграций необходимо находиться в папке `src`.
Также убедитесь, что у вас корректно установлена переменная среды `FLASK_APP`, она должна быть
равна `manage.py`:
```bash
echo $FLASK_APP
```
Должен быть результат:
```
manage.py
```
Если переменная `FLASK_APP` не установлена, то установите её:
```bash
echo FLASK_APP=manage.py
```
Сформировать файлы миграции:
```bash
python -m flask db migrate -m "Your comment"
```
Выполнить миграции:
```bash
python -m flask db upgrade
```


### Управление зависимостями
В качестве пакетного менеджера используется [Poetry version 1.2.0rc2](https://python-poetry.org/docs/1.2/#installation). Для управления зависимостями используются группы (см. файл `pyproject.toml`).

Все основные зависимости располагаются в группе `tool.poetry.dependencies`:
```
[tool.poetry.dependencies]
python = "^3.10"
Django = "^4.1"
```
Добавление основной зависимости:
```bash
poetry add pendulum
```
Остальные зависимости делятся на группы. Например, группа `lint` - зависимостей для линтинга:
```
[tool.poetry.group.lint.dependencies]
flake8 = "^5.0.4"
flake8-broken-line = "^0.5.0"
flake8-quotes = "^3.3.1"
pep8-naming = "^0.13.2"
```
Добавление зависимости в конкретную группу (использовать флаг `--group` и название группы):
```bash
poetry add pytest --group test
```


### Импорты
Выполняйте импорты из каталогов, вложенных в `src`. Следите, чтобы ваши импорты не начинались с папки `src`.
Например:
```
\
├── movies_auth
│   ├── src
│   │   ├── app
│   │   │   ├── auth
│   │   │   │   └── routes.py
│   │   │   └── models.py
│   │   └── manage.py
└── └── docker
```
Необходимо выполнить импорт моделей из файла `models.py` в файл `routes.py`.

Неправильно:
```python
from src.app.models import User
```
Правильно:
```python
from app.models import User
```
Если вы используете PyCharm, то вы можете пометить каталог `src` как `Source Root` (правой кнопкой -> Mark Directory as -> Mark as Source Root),
тогда PyCharm будет корректно добавлять импорты.

Такое использование импортов необходимо для корректной контейнеризации приложения в докере.
Внутри докер-контейнера папка приложения может называться по-другому, например, мы захотим назвать её `app`.
В Dockerfile это будет выглядеть так:
```dockerfile
ARG HOME_DIR=/app
WORKDIR $HOME_DIR

COPY ./src .
```
На хосте каталог называется `src`, а в контейнере `app`. Импорт из `src` приведет к ошибке:
```
ModuleNotFoundError: No module named 'src'
```


### Conventional Commits
Ваши комментарии к коммитам должны соответствовать [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
Pre-commit хук `conventional-pre-commit` выполнит проверку комментария перед коммитом.
Если ваш комментарий не соответствует конвенции, то в терминале вы увидите подобное сообщение:
```bash
commitizen check.........................................................Failed
- hook id: conventional-pre-commit
- exit code: 1
```
Для более удобного написания комментариев к коммитам, вы можете воспользоваться плагином
Conventional Commit для PyCharm:
![conventional-commit-plugin](docs/assets/img/PyCharm/conventional-commit-plugin.png)

### Настройки IDE
Проект содержит файл `.editorconfig` - ознакомьтесь с ним, чтобы узнать какие настройки должны быть в вашем редакторе.

Основное:
* максимальная длина строки: 100;
* отступы: пробелы;
* количество отступов: 4;


### Форматер и линтер
В качестве форматера мы используем [black](https://github.com/psf/black). Конфиг black см. в файле `pyproject.toml` в секции `[tool.black]`.
Линтер - flake8, конфиг находится в файле `setup.cfg`.

Если Вы используете PyCharm, то можете настроить форматирование файла с помощью black через External Tools:
![add-external-tool.png](docs/assets/img/PyCharm/add-external-tool.png)
Также можете повесить на это действие hot key:
![add-hot-key.png](docs/assets/img/PyCharm/add-hot-key.png)


<h2 align="center">Flow работы с проектом</h2>


- Форкаем проект
- В своем форке создаем новую ветку, делаем туда коммиты. Название ветки = название issue
- Когда все готово создаем PR в основной репо
- Прикрепляем PR к issue
- Проходим ревью
- Вливаем в ветку main (через squash & merge)
- Оповещаем всех остальных (чтобы они подтянули изменения из main и сразу порешали merge conflict)
