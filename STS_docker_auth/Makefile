PACKAGE = STS_docker_auth

VIRTUALENV = venv.$(PACKAGE)

venv:
	virtualenv $(VIRTUALENV)

init: 
	pip install -r requirements.txt

clean:
	find -name '*.pyc' -exec rm {} \;
