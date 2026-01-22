# Please note that this Docker file does not yet produce anything useful. Work In Progress
FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install swig -y

WORKDIR /app

# Install uv
RUN pip3 install uv

COPY . .

# Install dependencies using uv
RUN uv sync

RUN chmod +x ./start.sh
RUN mv .env.docker .env

# Install PDF converter
RUN apt-get update && apt-get install -y wkhtmltopdf

# Install node, npm and yarn for the JS side
RUN apt install nodejs -y
RUN apt install npm -y
RUN npm install --global yarn

# Make sure the PDF advice folder is available
RUN mkdir -p /tmp/data_questionnaire_agent/pdfs

CMD ["/bin/bash", "./run_app.sh"]