# Data Wellness Q&A Chatbot

This is a reverse chatbot that asks the users questions about data integration practices and then gives advice based on a body of knowledge.
This version operates a bit like an agent which tries to gather enough information to be able to give advice. So it may ask an unspecified number of questions.

We have used a specially changed version of the [Chainlit][https://chainlit.io] library that you can install from the wheels folder.

The source code for the hacked chainlit version is from this repo:

https://github.com/onepointconsulting/chainlit-data-wellness-agent.git

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

```cd 
poetry install
```

## UI Installation

You have to download the UI files (a React app from Github)

```
mkdir ~/projects/data-wellness-companion-ui
cd ~/projects/data-wellness-companion-ui
wget https://github.com/onepointconsulting/data-wellness-companion-ui/releases/download/v0.1/companion_ui.zip

cd ~/projects/data-wellness-companion
mkdir ui
cd ui
unzip ~/projects/data-wellness-companion-ui/companion_ui.zip
# Change the port to the port you are going to use. Here we change from 8085 to 8086
sed -i -e 's/8085/8086/g' ./index.html
sed -i -e 's/127\.0\.0\.1/<some_ip_address>/g' ./index.html
```

## Running

### Prepare the Postgres DB

Before you run for the first time, you will need to create the Postgres database. Execute this command to start psql (make sure Postgres is installed)

```
sudo -u postgres psql
```

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

And run the script below:

```
DROP TABLE IF EXISTS PUBLIC.TB_SESSION_CONFIGURATION;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTION_SUGGESTIONS;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTION;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTIONNAIRE_STATUS_SUGGESTIONS;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTIONNAIRE_STATUS;

CREATE TABLE PUBLIC.TB_QUESTIONNAIRE_STATUS (
	ID serial NOT NULL,
	SESSION_ID CHARACTER VARYING(36) NOT NULL,
	QUESTION CHARACTER VARYING(65535) NOT NULL,
	ANSWER CHARACTER VARYING(4096) NULL,
	FINAL_REPORT boolean, 
	CREATED_AT TIMESTAMP DEFAULT NOW(),
	UPDATED_AT TIMESTAMP DEFAULT NOW(),
	PRIMARY KEY (ID)
);

CREATE TABLE PUBLIC.TB_QUESTION (
	ID serial NOT NULL,
	QUESTION CHARACTER VARYING(1024) NOT NULL,
	PREFERRED_QUESTION_ORDER int NULL,
	PRIMARY KEY (ID)
);

CREATE TABLE PUBLIC.TB_QUESTION_SUGGESTIONS(
	ID serial NOT NULL,
	IMG_SRC CHARACTER VARYING(100) NOT NULL,
	IMG_ALT CHARACTER VARYING(256) NOT NULL,
	TITLE CHARACTER VARYING(256) NOT NULL,
	MAIN_TEXT CHARACTER VARYING(1024) NOT NULL,
	QUESTION_ID integer NOT NULL,
	PRIMARY KEY (ID),
	CONSTRAINT QUESTION_ID
		FOREIGN KEY (QUESTION_ID) REFERENCES PUBLIC.TB_QUESTION (ID) 
		MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID
);

CREATE TABLE PUBLIC.TB_SESSION_CONFIGURATION(
	ID serial NOT NULL,
	SESSION_ID CHARACTER VARYING(36) NOT NULL,
	CONFIG_KEY CHARACTER VARYING(36) NOT NULL,
	CONFIG_VALUE CHARACTER VARYING(255) NOT NULL
);

CREATE TABLE PUBLIC.TB_QUESTIONNAIRE_STATUS_SUGGESTIONS(
	ID serial NOT NULL,
	QUESTIONNAIRE_STATUS_ID INTEGER NOT NULL,
	MAIN_TEXT CHARACTER VARYING(2048) NOT NULL,
	PRIMARY KEY (ID),
	CONSTRAINT QUESTIONNAIRE_STATUS_ID
		FOREIGN KEY (QUESTIONNAIRE_STATUS_ID) REFERENCES PUBLIC.TB_QUESTIONNAIRE_STATUS (ID) 
		MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Initial question
INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER)
VALUES('Which area of your data ecosystem are you most concerned about?', 1);

-- Some suggestions for the initial screen
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('poor_data_quality.png', 'Poor data quality', 'Poor data quality', 'Low-quality data can lead to incorrect insights and poor decision-making.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));
	   
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('compliance_risks.png', 'Compliance and security risks', 'Compliance and security risks', 'Mishandling data can lead to legal troubles and reputational damage.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('data_silos.png', 'Data silos', 'Data silos', 'Data trapped in departmental silos can be inaccessible to other parts.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('lack_of_skilled_personnel.png', 'Lack of skilled personnel', 'Lack of skilled personnel', 'Missing skills in data science, analytics, AI and ML can impede the effective use of data.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('data_overload.png', 'Data overload', 'Data overload', '"Data glut" can slow down processes and make it difficult to identify what data is actually useful.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('cost_and_complexity.png', 'Cost and complexity', 'Cost and complexity', 'A robust data analytics infrastructure requires significant investment of resources.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('inconsistent_data_strategies.png', 'Inconsistent data strategies', 'Inconsistent data strategies', 'Difficult to align with modern concepts like Data Fabric, Mesh and Generative AI.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('resistence_to_change.png', 'Resistance to change', 'Resistance to change', 'Employees need to adapt to new ways of operating to make data-driven transformation work.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));
```

### Knowledge base 

The knowledge base is based on a directory (see environment variable `RAW_TEXT_FOLDER`). The folder needs to have *.txt documents in it.

The server fails if there are no documents in this folder.

### Running the main application

```
python ./data_questionnaire_agent/server/questionnaire_server_main.py
```

## Configuration

This is the content of the `.env` file, which needs to be saved in the project root folder.

```
OPENAI_API_KEY=<open-api-key>
# This model does not seem to perform too well.
# OPENAI_MODEL=gpt-4-1106-preview
OPENAI_MODEL=gpt-4-0613
REQUEST_TIMEOUT=300

VERBOSE_LLM=true
LANGCHAIN_CACHE=false
CHATGPT_STREAMING=false

UI_TIMEOUT = 60

# Email related
MAIL_FROM_PERSON=<mail sender>
MAIL_USER=<some valid email id>
MAIL_PASSWORD=<mail password>
MAIL_FROM=<some valid email sender>
MAIL_SERVER=smtp.gmail.com:587

# General stuff
PROJECT_ROOT=/development/playground/langchain/data_questionnaire_agent
QUESTION_CACHE_FOLDER=/tmp/data_questionnaire_agent/cache

# PDF Related
WKHTMLTOPDF_BINARY=/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe
TEMPLATE_LOCATION=/development/playground/langchain/data_questionnaire_agent/templates
PDF_FOLDER=/tmp/data_questionnaire_agent/pdfs

# Whether to show the task list or not
TASKLIST=false

# UI
SHOW_CHAIN_OF_THOUGHT=true

# Embedding related
# The following property is where your knowledge base is located
RAW_TEXT_FOLDER=/development/playground/langchain/data_questionnaire_agent/docs/raw_text
EMBEDDINGS_PERSISTENCE_DIR=/development/playground/langchain/data_questionnaire_agent/embeddings
EMBEDDINGS_CHUNK_SIZE=2500
SEARCH_RESULTS_HOW_MANY=2

# Question generation related
QUESTIONS_PER_BATCH=1
# Minimum questions asked before giving advice
MINIMUM_QUESTIONNAIRE_SIZE=4

# Token limit for chatgpt 4. Important to extend the context as much as possible using the vector DB search
# This could be higher as the TPM increased on the 6th of November
TOKEN_LIMIT=6000

# Not in use
IMAGE_LLM_TEMPERATURE=0.9

# Show session cost
SHOW_SESSION_COST=false
OPENAI_RETRY_ATTEMPTS=3
OPENAI_WAIT_FIXED=30

# SQLLite DB related
# Optional
ONEPOINT_SQL_LITE_DB=/tmp/SQL_LITE_DB.db

# Related to the tracker DB download
TRACKER_DB_LOGS_PASSWORD=<pass>

# Database related
DB_NAME=data_wellness_companion
DB_USER=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
DB_PASSWORD=<pwd>

# Websocket server related
WEBSOCKET_SERVER=0.0.0.0
WEBSOCKET_PORT=8085
WEBSOCKET_CORS_ALLOWED_ORIGINS=*

# Webserver related
UI_FOLDER=/development/playground/langchain/data_questionnaire_agent/web/ui
```

## Running Tests

You can run tests like this:

```bash
pytest
```