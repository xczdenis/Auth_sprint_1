template = {
    "info": {
        "title": "Auth service for movies",
        "version": "1.0",
    },
    "securityDefinitions": {
        "bearer": {
            "description": """Для защищенных маршрутов, в запросе должен передаваться
JWT токен в заголовке 'Authorization'.
JWT токен необходимо получить, используя маршрут auth/login, передав действительные логин и пароль.
Заголовок 'Authorization'должен иметь следующий синтаксис:
```
Bearer xxxxxx.yyyyyyy.zzzzzz
```
""",
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
    "consumes": [
        "application/json",
    ],
    "produces": [
        "application/json",
    ],
    "definitions": {
        "DefaultMsgResponse": {"type": "object", "properties": {"msg": {"type": "string"}}},
        "Response401_access": {
            "description": "В заголовке запроса не передан access_token, либо он не корректный, "
            "либо его срок действия истек",
            "schema": {"$ref": "#/definitions/DefaultMsgResponse"},
            "examples": {"msg": "Token has expired"},
        },
        "Response401_refresh": {
            "description": "В заголовке запроса не передан refresh_token, либо он не корректный, "
            "либо его срок действия истек",
            "schema": {"$ref": "#/definitions/DefaultMsgResponse"},
            "examples": {"msg": "Token has expired"},
        },
        "Response403": {
            "description": "У пользователя недостаточно прав на выполнение операции",
            "schema": {"$ref": "#/definitions/DefaultMsgResponse"},
            "examples": {"msg": "Permission denied"},
        },
        "Response422_access": {
            "description": "Не корректная сигнатура access токена",
            "schema": {"$ref": "#/definitions/DefaultMsgResponse"},
            "examples": {"msg": "Signature verification failed"},
        },
        "Response422_refresh": {
            "description": "Не корректная сигнатура refresh токена",
            "schema": {"$ref": "#/definitions/DefaultMsgResponse"},
            "examples": {"msg": "Signature verification failed"},
        },
        "PermissionsDetail": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "format": "uuid", "description": "ID разрешения"},
                "name": {"type": "string", "description": "Название разрешения"},
                "codename": {"type": "string", "description": "Уникальный код разрешения"},
            },
        },
        "PermissionsList": {
            "type": "array",
            "items": {"$ref": "#/definitions/PermissionsDetail"},
        },
        "PermissionsDetailResponse": {
            "type": "object",
            "properties": {
                "data": {"$ref": "#/definitions/PermissionsDetail"},
            },
        },
        "PermissionsListResponse": {
            "type": "object",
            "properties": {
                "data": {"$ref": "#/definitions/PermissionsList"},
            },
        },
    },
}
