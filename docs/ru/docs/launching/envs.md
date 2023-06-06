# Окружения dev и prod

Основной тип запуска проекта - через docker-compose. Запуск проекта может быть выполнен в одном
из двух окружений: `development` или `production`. Окружение управляется настройкой `ENVIRONMENT` в
файле `.env`:
```bash
ENVIRONMENT=development
```

Если настройка `ENVIRONMENT` имеет значение `production`, то при запуске используется файл
`docker-compose.yml`. Если настройка `ENVIRONMENT` имеет значение `development`, то при
запуске используется дополнительный файл `docker-compose.dev.yml`.

При запуске в режиме `development` папка приложения `src` монтируется как том, а каждый сервис
имеет `expose` порты:
```dockerfile
# docker-compose.dev.yml

x-base-dev-service: &base-dev-service
    restart: "no"

services:
    postgres:
        <<: *base-dev-service
        ports:
            - ${POSTGRES_PORT}:5432

    redis:
        <<: *base-dev-service
        ports:
            - ${REDIS_PORT}:6379
```


## Один Dockerfile для двух окружений

Стоит обратить внимание на `Dockerfile` для `Flask` приложения. Помимо `multistage` сборки, данный файл
использует слои `development` и `production` в соответствии с
настройкой `ENVIRONMENT`:
```dockerfile
# ./docker/movies_auth/Dockerfile

ARG env=production
...

FROM final as development


FROM final as production

COPY ./src/${pckg_name} ./src/${pckg_name}


FROM ${env}

ENTRYPOINT ["./scripts/entrypoint.sh"]
```

Данная конфигурация позволяет использовать разные итоговые образы в зависимости от режима запуска. При запуске
в режиме `development` папка приложения [src](src) монтируется как том в файле [docker-compose.dev.yml](docker-compose.dev.yml),
поэтому слой `development` в `Dockerfile` пустой:
```dockerfile
# ./docker/movies_auth/Dockerfile
...

FROM final as development

...
```
При запуске в окружении `production` папка приложения [src](src) копируется с помощью инструкции `COPY`:
```dockerfile
# ./docker/movies_auth/Dockerfile
...

FROM final as production

COPY ./src/${pckg_name} ./src/${pckg_name}
```
В конце файла, выбирается образ из переменной `env`:
```dockerfile
# ./docker/python/Dockerfile
ARG env=production
...

FROM ${env}
```

Переменная `env` в свою очередь передается как аргумент сборки:
```dockerfile
# ./docker-compose.yml
services:
    app:
        build:
            context: .
            dockerfile: ./docker/movies_auth/Dockerfile
            args:
                - env=${ENVIRONMENT}
```
Итоговый образ будет использовать самый последний слой. Таким образом, если настройка `ENVIRONMENT` имеет
значение `development`, то будет использован образ `development`, а если `production`, то `production`.
