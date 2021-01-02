FROM registry:2

COPY cleanup_server.py .
COPY config.yml /etc/docker/registry/config.yml

CMD ["/./cleanup_server.py"]
