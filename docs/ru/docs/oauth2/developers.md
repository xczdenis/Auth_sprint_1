# OAuth2 для разработчиков

!!!info "Для кого этот раздел"
    В данном разделе приведена информация для разработчиков сервиса Auth-movies.


## Intro
Все, что необходимо для работы с OAuth2 находится в папке `src/app/oauth2`.

## Requirements
Используется библиотека [authlib](https://github.com/lepture/authlib)

## Конфиги провайдеров
Каждый OAuth провайдер имеет свои `client_id` и `secret_id`. Эти настройки нужно добавить в
переменные окружения в папке `.envs`. Например:
```dotenv
GOOGLE_CLIENT_ID=c1b2
GOOGLE_CLIENT_SECRET=f030d
```
Затем необходимо добавить эти переменные в настройки приложения:
```python hl_lines="8-9"
# src/config.py


class Settings(BaseSettings):
    PROJECT_NAME: str = "movies_auth"
    SECRET_KEY: str
    ...
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
```

## Создание адаптера для провайдера
Каждый провайдер имеет свои уникальные настройки, начиная с адреса api, заканчивая местом
расположения `access_token` в запросе. Работа с провайдерами реализована через адаптеры.

Для примера рассмотрим адаптер `GoogleOAuthProvider`:
```python
# src/app/oauth2/base.py


@dataclass
class GoogleOAuthProvider(BaseOAuthProvider):
    name: str = "google"
    userinfo_endpoint: str = "userinfo?alt=json"
    authorize_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    access_token_url: str = "https://oauth2.googleapis.com/token"
    api_base_url: str = "https://www.googleapis.com/oauth2/v1/"
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
Для добавления нового провайдера нужно создать для него адаптер. На что следует обратить внимание:

Реквизит `name`: формируется из имени настроек `EXAMPLE_CLIENT_ID`. Для провайдера Google,
настройка называется `GOOGLE_CLIENT_ID`, значит значение реквизита name должно быть `google`.

Реквизит `userinfo_endpoint`: путь, по которому отправляется запрос на получение информации из
аккаунта пользователя. Полный url запроса формируется как `api_base_url` + `userinfo_endpoint`.
Получение данных пользователя выполняется в методе `get_user_info` базового класса
`BaseOAuthProvider` (метод может быть переопределен в адаптере):
```python hl_lines="5-7"
@dataclass
class BaseOAuthProvider:
    ...

    def get_user_info(self) -> dict:
        r = self._client.get(self.userinfo_endpoint)
        return r.json()
```

Адаптер должен содержать метод `get_social_account`, который возвращает экземпляр класса
`SocialAccount`.

Реквизит `client_kwargs` может содержать уникальные настройки, требуемые для провайдера. Например,
для google требуется указать `scope` (разрешения), а для mail требуется указать место расположения
`access_token`:
```python hl_lines="8"
@dataclass
class MailOAuthProvider(BaseOAuthProvider):
    name: str = "mail"
    userinfo_endpoint: str = "userinfo"
    authorize_url: s-tr = "https://oauth.mail.ru/login"
    access_token_url: str = "https://oauth.mail.ru/token"
    api_base_url: str = "https://oauth.mail.ru"
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
