# OAuth2 для разработчиков

!!!info "Для кого этот раздел"
    В данном разделе приведена информация для разработчиков сервиса Auth-movies.


## Intro
Все, что необходимо для работы с OAuth2 находится в папке `src/app/oauth2`.

## Requirements
Используется библиотека [authlib](https://github.com/lepture/authlib)

## Конфиги провайдеров
Настройки OAuth провайдеров хранятся в файлах `.env` в папке `.envs`. Рассмотрим подробнее
структуру настроек на примере одного из провайдеров:
```
YANDEX_CLIENT_ID=c95621
YANDEX_CLIENT_SECRET=s389752f
YANDEX_OAUTH__AUTHORIZE_URL=https://oauth.yandex.ru/authorize
YANDEX_OAUTH__ACCESS_TOKEN_URL=https://oauth.yandex.ru/token
YANDEX_OAUTH__API_BASE_URL=https://login.yandex.ru
YANDEX_OAUTH__USERINFO_URL=info
```
Каждый OAuth провайдер имеет свои `client_id` и `secret`. Имя переменной окружения
для этих параметров формируется по маске `EXAMPLE_CLIENT_ID`, `EXAMPLE_SECRET`,
где `EXAMPLE` - это имя провайдера.

!!!warning
    Библиотека authlib будет использовать имя `EXAMPLE` как атрибут экземпляра класса провайдера

Затем следует блок переменных с префиксом `EXAMPLE_OAUTH__` - эти настройки будут преобразованы
в словарь в объекте `settings`:
```python
{
    'yandex_oauth': {
        'authorize_url': 'https://oauth.yandex.ru/authorize',
        'access_token_url': 'https://oauth.yandex.ru/token',
        'api_base_url': 'https://login.yandex.ru',
        'userinfo_url': 'info'
    }
}
```
Для этого, провайдер должен быть добавлен в `settings` следующим образом:
```python hl_lines="15"
# src/config.py


class BaseOAuthProvider(BaseModel):
    authorize_url: str
    access_token_url: str
    api_base_url: str
    userinfo_url: str


class Settings(BaseSettings):
    PROJECT_NAME: str = "movies_auth"
    SECRET_KEY: str
    ...
    YANDEX_OAUTH: BaseOAuthProvider
```

## Создание адаптера для провайдера
Каждый провайдер имеет свои уникальные настройки, начиная с адреса api, заканчивая местом
расположения `access_token` в запросе. Работа с провайдерами реализована через адаптеры.

Для примера рассмотрим адаптер `GoogleOAuthProvider`:
```python
# src/app/oauth2/base.py


@dataclass
class GoogleOAuthProvider(BaseOAuthProvider):
    name: str = OAuthProviders.google
    client_kwargs: dict = field(
        default_factory=lambda: {
            "scope": "https://www.googleapis.com/auth/userinfo.email "
            "https://www.googleapis.com/auth/userinfo.profile"
        }
    )

    def get_social_account(self) -> SocialAccount | None:
        user_info = self.get_user_info()
        if user_info:
            return SocialAccount(
                id=user_info["id"],
                email=user_info["email"],
                login=user_info["email"],
                name=user_info["given_name"],
            )
        return None
```
Для добавления нового провайдера нужно создать для него адаптер - наследник класса
`BaseOAuthProvider`. Имя нового провайдера нужно указать в классе `OAuthProviders`:
```python
# src/app/oauth2/base.py


@dataclass(slots=True, frozen=True)
class OAuthProviders:
    yandex = "yandex"
    mail = "mail"
    google = "google"
```

На что следует обратить внимание при создании адаптера:

* **Имя провайдера**: оно формируется из имени настроек `EXAMPLE_CLIENT_ID`. Для провайдера Google,
настройка называется `GOOGLE_CLIENT_ID`, значит имя должно быть `google`.

* Получение данных пользователя выполняется в методе `get_user_info` базового класса
`BaseOAuthProvider` (метод может быть переопределен в адаптере):
```python hl_lines="5-7"
@dataclass
class BaseOAuthProvider:
    ...

    def get_user_info(self) -> dict:
        r = self._client.get(self.userinfo_endpoint)
        return r.json()
```

* Адаптер должен содержать метод `get_social_account`, который возвращает экземпляр класса
`SocialAccount`.

* Реквизит `client_kwargs` может содержать уникальные настройки, требуемые для провайдера. Например,
для google требуется указать `scope` (разрешения), а для mail требуется указать место расположения
`access_token`:
```python hl_lines="4"
@dataclass
class MailOAuthProvider(BaseOAuthProvider):
    name: str = OAuthProviders.mail
    client_kwargs: dict = field(default_factory=lambda: {"token_placement": "uri"})
```

## Регистрация провайдера
Для того чтобы провайдер начал действовать, его нужно зарегистрировать в приложении.
Сначала нужно создать экземпляр провайдера в файле `src/app/oauth2/__init__.py`:
```python
# src/app/oauth2/__init__.py

from app.oauth2 import base

oauth_manager = base.OAuthManager()

yandex_oauth = base.YandexOAuthProvider()
mail_oauth = base.MailOAuthProvider()
google_oauth = base.GoogleOAuthProvider()
```
Затем, в функции `create_app()` нужно зарегистрировать нового провайдера:
```python hl_lines="11-13"
# src/app/__init__.py

from app.oauth2 import oauth_manager, yandex_oauth, mail_oauth, google_oauth


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    oauth_manager.init_app(app, cache=redis_db)
    oauth_manager.register_provider(yandex_oauth)
    oauth_manager.register_provider(mail_oauth)
    oauth_manager.register_provider(google_oauth)
```
На этом добавление нового провайдера завершено.
