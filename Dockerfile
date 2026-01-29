FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]

RUN apt update \
 && apt install -y \
      python3 \
      python3-pip \
      swig \
      git

WORKDIR /app

# Install uv (allow installing into the system Python in this container)
RUN pip3 install --break-system-packages uv

COPY . .

# Install dependencies using uv
RUN uv sync

# Install PDF converter
RUN apt-get update && apt-get install -y wkhtmltopdf ca-certificates curl gnupg

# Install Node.js 22 and yarn for the JS side
ENV NODE_MAJOR=22
RUN mkdir -p /etc/apt/keyrings \
 && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
 && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" > /etc/apt/sources.list.d/nodesource.list \
 && apt-get update \
 && apt-get install -y nodejs \
 && npm install --global yarn

# Make sure the PDF advice folder is available
RUN mkdir -p /tmp/data_questionnaire_agent/pdfs

# Run yarn inside of the data-wellness-companion-ui folder
RUN cd data-wellness-companion-ui && yarn
RUN cd data-wellness-companion-ui && yarn run build

# Copy the dist folder to the root folder
COPY data-wellness-companion-ui/dist /app/ui

# Copy the run_app.sh file to the root folder
COPY run_app.sh run_app.sh

CMD ["/bin/bash", "./run_app.sh"]