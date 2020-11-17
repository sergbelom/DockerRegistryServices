PACKAGE = STS_docker_auth

VIRTUALENV = venv.$(PACKAGE)

venv:
	virtualenv $(VIRTUALENV)

init: 
	pip install -r requirements.txt

clean:
	find -name '*.pyc' -exec rm {} \;
	docker rm -f sergbelom/sts_docker_auth

build: 
	docker build . --tag sergbelom/sts_docker_auth

run: 
	docker run --volume ${PWD}/certs:/certs --publish 5001:5001 sergbelom/sts_docker_auth

stop: 
	docker stop sergbelom/sts_docker_auth
