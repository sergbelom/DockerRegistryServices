clean:
	find -name '*.pyc' -exec rm {} \;
	docker rm -f sts_listener_server

build: 
	docker build . --tag sergbelom/sts_listener_server

run: 
	docker run --entrypoint /bin/bash sergbelom/sts_listener_server

stop: 
	docker stop sts_listener_server

compose:
	docker-compose down
	docker-compose build
	docker-compose up
