PACKAGE = STS_docker_auth

VIRTUALENV = venv.$(PACKAGE)

venv:
	virtualenv $(VIRTUALENV)

init: 
	pip install -r requirements.txt

clean:
	find -name '*.pyc' -exec rm {} \;
	docker rm -f sts_docker_auth

build: 
	docker build . --tag sergbelom/sts_docker_auth

run: 
	docker run --entrypoint /bin/bash sergbelom/sts_docker_auth

stop: 
	docker stop sts_docker_auth

compose:	
	docker-compose down
	docker-compose build
	docker-compose up
