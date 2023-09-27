# Data Integration Questionnaire Agent

This is a reverse chatbot that asks the users questions about data integration practices and then gives advice based on a body of knowledge.
This version operates a bit like an agent which tries to gather enough information to be able to give advice. So it may ask an unspecified number of questions.

## Setup

We suggest to use [Conda](https://docs.conda.io/en/latest/) to manage the virtual environment and then install poetry.

```
conda activate base
conda remove -n data_integration_questionnaire_agent --all
conda create -n data_integration_questionnaire_agent python=3.11
conda activate data_integration_questionnaire_agent
pip install poetry
poetry init
```

## Installation

```
poetry install
poetry add --editable \\wsl.localhost\Ubuntu\home\gilf\projects\chainlit-2023-september\backend\dist\chainlit-0.7.1-py3-none-any.whl
```

## Running


Coming soon:

```
chainlit run .\data_questionnaire_agent\ui\data_questionnaire_chainlit.py --port 8080
```

This is not yet implemented.


## Configuration

```
OPENAI_API_KEY=<open_ai_key>
# OPENAI_MODEL=gpt-3.5-turbo-0613
OPENAI_MODEL=gpt-4-0613
# OPENAI_MODEL=gpt-4-32k-0613
REQUEST_TIMEOUT=140

VERBOSE_LLM=true
LANGCHAIN_CACHE=false

UI_TIMEOUT = 2400

# Email related
MAIL_FROM_PERSON=Gil Fernandes
MAIL_USER=<email>
MAIL_PASSWORD=<password>
MAIL_FROM=<email>
MAIL_SERVER=smtp.gmail.com:587

# General stuff
PROJECT_ROOT=C:/development/playground/langchain/data_integration_questionnaire
QUESTION_CACHE_FOLDER=c:/tmp/data_integration_questionnaire/cache

# PDF Related
WKHTMLTOPDF_BINARY=C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe
TEMPLATE_LOCATION=C:/development/playground/langchain/data_integration_questionnaire/templates
PDF_FOLDER=C:/tmp/data_integration_questionnaire/pdfs

# Whether to show the task list or not
TASKLIST=false

# The knowledge base path
KNOWLEDGE_BASE_PATH=C:/development/playground/langchain/data_integration_questionnaire/docs/knowledge_base.txt

# UI
SHOW_CHAIN_OF_THOUGHT=true

# Embedding related
RAW_TEXT_FOLDER=C:\development\playground\langchain\data_integration_questionnaire\docs\raw_text
EMBEDDINGS_PERSISTENCE_DIR=C:\development\playground\langchain\data_integration_questionnaire\embeddings
EMBEDDINGS_CHUNK_SIZE=2500
SEARCH_RESULTS_HOW_MANY=4

# Question generation related
QUESTIONS_PER_BATCH=2

```