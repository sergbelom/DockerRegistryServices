FROM python
COPY STS_docker_auth.py .
COPY requirements.txt .
COPY users.auth .
RUN pip install -r requirements.txt
CMD ["/./STS_docker_auth.py"]
