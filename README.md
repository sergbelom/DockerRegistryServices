
**Развертывание сервера авторизации docker_auth**


1. Сертификаты.


    `mkdir -p docker_auth_certificates`

    `openssl req -newkey rsa:4096 -nodes -keyout docker_auth_certificates/server.key -x509 -days 365 -out docker_auth_certificates/server.pem -subj "/C=EU/ST=Germany/L=Freiburg/O=registry/CN=localhost"`


2. Получаем пример конфигурации docker_auth сервера


    `mkdir -p docker_auth_config`

    ```
    if [[ ! -f docker_auth_config/simple.yml ]]; then
        curl --fail --location --output docker_auth_config/simple.yml https://github.com/cesanta/docker_auth/raw/master/examples/simple.yml
    fi
    sed -i 's|/path/to/|/ssl/|g' docker_auth_config/simple.yml
    ```


3. Запуск registry-pod 


    `docker run -d --name registry-pod --publish 127.0.0.1:5000:5000 --publish 127.0.0.1:5001:5001 alpine sh -c 'while true; do sleep 10; done'`


4. Запуск docker_auth


    `docker run -d --name registry-auth --network container:registry-pod --mount type=bind,src=$(pwd)/docker_auth_config,dst=/config,readonly --mount type=bind,src=$(pwd)/docker_auth_certificates,dst=/ssl,readonly --env TZ=Europe/Berlin cesanta/docker_auth:1 --v=2 --alsologtostderr /config/simple.yml`


5. Запуск registry:2.6.2 (на дефолтном registry:2 не работает из-за бага в docker)


    `docker run -d --name registry-registry --network container:registry-pod --mount type=bind,src=$(pwd)/docker_auth_certificates,dst=/ssl,readonly --env TZ=Europe/Berlin --env REGISTRY_AUTH=token --env REGISTRY_AUTH_TOKEN_REALM=https://localhost:5001/auth --env REGISTRY_AUTH_TOKEN_SERVICE="Docker registry" --env REGISTRY_AUTH_TOKEN_ISSUER="Acme auth server" --env REGISTRY_AUTH_TOKEN_ROOTCERTBUNDLE=/ssl/server.pem registry:2.6.2`


6. Команды для тестирования:


- login и logout в сервис авторизации

    `docker login localhost:5000`

    `docker logout localhost:5000`

    - существующие пользователи:

        user: admin  password: badmin

        user: test password: 123

- тестовый образ для push pull операций в registry:

    `docker pull ubuntu:latest`

    `docker tag ubuntu:wily localhost:5000/my/ubuntu:latest`

    `docker push localhost:5000/my/ubuntu:latest`

    `docker pull localhost:5000/my/ubuntu:latest`


7. Остановить и удалить контейнеры.


    `docker container stop registry-pod && docker container rm -v registry-pod`
    
    `docker container stop registry-auth && docker container rm -v registry-auth`
    
    `docker container stop registry-registry && docker container rm -v registry-registry`
