FROM python:3.11.4-alpine

COPY requirements.txt /

RUN ["pip", "install", "-r", "requirements.txt"]

COPY . /

CMD [ "python" ,"./server.py"]