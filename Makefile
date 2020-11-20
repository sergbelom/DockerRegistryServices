run: 
	docker-compose down
	docker-compose build
	docker-compose up

build: 
	docker build STS_docker_auth/ --tag sergbelom/sts_docker_auth
