FROM python:2
COPY requirements.txt .
COPY users.auth .
RUN pip install -r requirements.txt
COPY STS_docker_auth.py .
CMD ["/./STS_docker_auth.py"]
