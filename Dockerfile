FROM python:3.8.5
WORKDIR /code
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN apt update
RUN apt install -y gettext
COPY . .

