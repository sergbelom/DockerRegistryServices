run: 
	docker-compose down
	docker-compose build
	docker-compose up

build: 
	docker build STS_docker_auth/ --tag sergbelom/sts_docker_auth
	docker build STS_listener_server/ --tag sergbelom/sts_listener_server
	docker build STS_listener_server/ --tag sergbelom/sts_listener_server
	docker build Cleanup_server/ --tag sergbelom/cleanup_server
	docker build Space_available_server/ --tag sergbelom/space_available_server

clean:
	find -name '*.pyc' -exec rm {} \;
	docker rm -f sts_docker_auth
	docker rm -f sts_docker_auth_registry_1
	docker rm -f sts_listener_server
	docker rm -f sts_docker_auth_cleanup_server_1
	docker rm -f sts_docker_auth_space_available_server_1

stop: 
	docker stop sts_docker_auth
	docker stop sts_docker_auth_registry_1
	docker stop sts_listener_server
	docker stop sts_docker_auth_cleanup_server_1
	docker stop sts_docker_auth_space_available_server_1

remove: 
	docker rmi sergbelom/sts_listener_server
	docker rmi sergbelom/sts_docker_auth
	docker rmi sergbelom/cleanup_server
	docker rmi sergbelom/space_available_server

prune: 
	docker image prune
