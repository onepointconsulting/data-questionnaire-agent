# Please note that this Docker file does not yet produce anything useful. Work In Progress
FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install python3.12-venv -y
RUN apt install swig

WORKDIR /app

RUN python3 -m venv venv
RUN . venv/bin/activate
RUN ./venv/bin/pip install poetry

COPY . .

RUN ./venv/bin/poetry install

RUN chmod +x ./start.sh

CMD ["/bin/bash", "./start.sh"]