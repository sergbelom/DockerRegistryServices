run: 
	docker-compose down
	docker-compose build
	docker-compose up

build: 
	docker build STS_docker_auth/ --tag sergbelom/sts_docker_auth
	docker build STS_listener_server/ --tag sergbelom/sts_listener_server
	docker build Ros_images/ros_1/ --tag firstros
	docker build Ros_images/ros_2/ --tag secondros

clean:
	find -name '*.pyc' -exec rm {} \;
	docker rm -f sts_docker_auth
	docker rm -f sts_docker_auth_registry_1
	docker rm -f sts_listener_server

stop: 
	docker stop sts_docker_auth
	docker stop sts_docker_auth_registry_1
	docker stop sts_listener_server

remove: 
	docker rmi firstros
	docker rmi secondros
	docker rmi sergbelom/sts_listener_server
	docker rmi sergbelom/sts_docker_auth

prune: 
	docker image prune
