run: 
	docker-compose up -d

build: 
	docker build STS_docker_auth/ --tag sergbelom/sts_docker_auth
