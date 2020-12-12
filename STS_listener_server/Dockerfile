FROM python:3
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY STS_listener_server.py .
CMD ["/./STS_listener_server.py"]
