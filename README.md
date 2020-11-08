**Сервис авторизации на основе JSON token с приватным Docker Registry**


Dokcer позволяет локально развернуть приватное хранилище образов Docker Registry.

Доступ к Docker Registry можно реализовать на основе токен аутентификации.

Возможность разработки такого сервиса описана в [документации](https://docs.docker.com/registry/spec/auth/token/).


**Сущесвующие сервисы авторизации**


Сущесвтует готовое решение [docker_auth](https://github.com/cesanta/docker_auth) разработанное на Go, которое позволяет настроить авторизацию с помощью разлчиных методов (лист пользователей, gooogle авторизация, github авторизация и т.п.)

Разработка собственного решения обоснована необходимостью иметь встроенный сервис авторизации, как часть SLAM Testing Service (STS), написанного на C++.


**Сервис авторизации STS_docker_auth**

Сервис авторизации разработан на python для токен-автризации на основе JSON web token.


**Команды для разворачивания STS_docker_auth**

1. Создать HOSTNAME

export HOSTNAME=$(hostname)

2. Сертификаты. Для работы docker registry и cервис авторизации необходимо [настроить сертификаты](https://docs.docker.com/registry/insecure/).

    `openssl genrsa -out certs/STS_docker_auth.key 2048`

    `openssl req -new -x509 -sha256 -key certs/STS_docker_auth.key -out certs/STS_docker_auth.crt -days 365 -subj "/O=sergbelom/OU=Auth/CN=${HOSTNAME}"`

Скопировать сертификаты из certs/*.crt в /usr/local/share/ca-certificates/

    sudo update-ca-certificates

Перезапустить docker сервис для обновления сертификатов

    sudo service docker restart

3. Запустить сервис авторизации STS_docker_auth и Docker Registry.

В каталоге STS_docker_auth необходимо:

- создать python окружение

    `make venv && . venv.authserver/bin/activate`

- установить необходимые пакеты (flask, pyjwt, pycrypto, cryptography)

    `make init`

- запустить сервис

    `./STS_docker_auth.py`

- запустить Docker Registry

    `docker-compose up -d`


4. Авторизация. 

JSON с доступными пользователями находится в STS_docker_auth/users.auth

- login и logout в сервис авторизации:

    `docker login https://${HOSTNAME}:5000`

    `docker logout https://${HOSTNAME}:5000`

- создание тега существующего образа для Docker Registry:

    `docker pull ubuntu:latest`

    `docker tag ubuntu:wily ${HOSTNAME}:5000/my/ubuntu:latest`

- команды pull и push для Docker Registry:

    `docker push ${HOSTNAME}:5000/my/ubuntu:1.0.0`

    `docker pull ${HOSTNAME}:5000/my/ubuntu:1.0.0`

если пользователь авторизован, то команды pull и push будут проходить успешно
