
**Intro**

Registry поддерживает отправку webhooks в ответ на события, происходящие в registry.

Уведомления отправляются в ответ на

- manifest pushes и pulls;

- layer pushes и pulls.

Эти действия сериализуются в события.

События помещаются в очередь во внутреннюю широковещательную систему registry, которая ставит в очередь и отправляет события к Endpoints.

Уведомления отправляются на конечные точки через HTTP-запросы. Каждая настроенная конечная точка имеет изолированные очереди, конфигурацию повторных попыток и цели http в каждом экземпляре registry. Когда в registry происходит действие, оно преобразуется в событие, которое помещается в памяти очереди. Когда событие достигает конца очереди, к конечной точке отправляется HTTP-запрос, пока запрос не будет успешным. События отправляются последовательно на каждую конечную точку, но порядок не гарантируется.

**Configuration**

Чтобы настроить экземпляр реестра для отправки уведомлений конечным точкам, необходимо добавить их в конфигурацию.


**Пример настройки нотификации в config.yml**

```
notifications

notifications:
  events:
    includereferences: true
  endpoints:
    - name: alistener
      disabled: false
      url: https://my.listener.com/event
      headers: 
      timeout: 1s
      threshold: 10
      backoff: 1s
      ignoredmediatypes:
        - application/octet-stream
      ignore:
        mediatypes:
           - application/octet-stream
        actions:
           - pull
```
**Пример запуска с конфигурцией**

docker run -p 5000:5000 \
            --name registry-registry \
            -v `pwd`/config.yml:/etc/docker/registry/config.yml \
             registry:2

**Проблемы:**

Не приходят сообщения на STS_listener_server

Воспроизведение:

В консоли перейти в корневую директории STS_docker_auth:

1 построить STS_docker_auth и STS_listener_server

  make build

2 запустить конфейнеры в одной сети 

  make run

Результат: запустится три контейнера (sts_docker_auth_registry_1, sts_docker_auth и sts_listener_server).

Логин в registry будет работать, если настроены сертификаты.

Контейнеры запускаются согласно docker-compose.yml

Нотификация настраивается в config.yml

3 Открыть другую консоль, залогиниться и запушить в registry

docker login https://${HOSTNAME}:5000

docker push ${HOSTNAME}:5000/my/ubuntu:latest

Результат: в консоли с запущенными контейнерами будет лог с попытками отправить сообщение на http://0.0.0.0:8086/log, но логи listener_log/log.log при этом пустые

Вопросы:

Пуллы приходят в начале загрузки образа?
Можно ли как-нибудь по ним установить, какой образ начинает загружаться и каков его размер?
Установить факт того, что пользователь прервал загрузку.
