
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

```
  notifications:
    endpoints:
      - name: alistener
        url: http://127.0.0.1:5000/
        headers:
          Authorization: [Bearer <your token, if needed>]
        timeout: 500ms
        threshold: 5
        backoff: 1s
```


Полный пример:

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



docker run -p 5000:5000 \
            --name registry-registry \
            -v `pwd`/config.yml:/etc/docker/registry/config.yml \
             registry:2

