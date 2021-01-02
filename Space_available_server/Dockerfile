FROM registry:2

COPY space_available_server.py .
COPY config.yml /etc/docker/registry/config.yml

CMD ["/./space_available_server.py"]