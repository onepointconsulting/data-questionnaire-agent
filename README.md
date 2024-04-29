# Data Wellness Q&A Chatbot

This is a reverse chatbot that asks the users questions about data integration practices and then gives advice based on a body of knowledge.
This version operates a bit like an agent which tries to gather enough information to be able to give advice. So it may ask an unspecified number of questions.

We have used a specially changed version of the [Chainlit][https://chainlit.io] library that you can install from the wheels folder.

The source code for the hacked chainlit version is from this repo:

https://github.com/onepointconsulting/chainlit-data-wellness-agent.git

## Cloning the project 

You should clone the project and then initialize the UI module with these commands:

```
git submodule init
git submodule update
```

## Setup

We suggest to use [Conda](https://docs.conda.io/en/latest/) to manage the virtual environment and then install poetry.

```
conda activate base
conda remove -n data_wellness_agent --all
conda create -n data_wellness_agent python=3.11
conda activate data_wellness_agent
pip install poetry
```

## Installation

Change the directory to the root folder of the project.

``` 
poetry install
```

## UI Installation

Before you run, you should compile the UI with this command from the root folder of the project. 
Please note that this requires the installation of Yarn and node 18.18.0 or later.

```
poetry run build-ui
```

The UI connects the websocket to port 8085 natively. If the Python server runs on a different port, please change the port accordingly.

## Running

### Prepare the Postgres DB

Before you run for the first time, you will need to create the Postgres database. Execute this command to start psql (make sure Postgres is installed)

On Linux you can install Postgres like this:

```
sudo -u postgres psql
```

On Windows you will need to download the distribution from here: https://www.postgresql.org/download/

Then create the database:

```
CREATE DATABASE data_wellness_companion
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
```

and add the initial tables with some data after exiting psql:

Run on the console:

```
sudo -u postgres psql data_wellness_companion
```

And run the script sql/db_setup.sql


### Knowledge base 

The knowledge base is based on a directory (see environment variable `RAW_TEXT_FOLDER`). The folder needs to have *.txt documents in it.

The server fails if there are no documents in this folder.

## Configuration

You will have to have a `.env` file. To get you started you can copy the `.env.local` to `.env` and then change the configuration parameters accordingly.

You will need to have an OpenAI API key.

### Running the main application

Make the Postgres DB is available.

```
python ./data_questionnaire_agent/server/questionnaire_server_main.py
```

You can then check the UI on http://localhost:8085/index.html

On Windows you can use the `.\start.ps1` script to start the server.

## Running Tests

You can run tests like this:

```bash
pytest
```