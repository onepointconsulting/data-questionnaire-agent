# Data Wellness Q&A Chatbot

This is a reverse chatbot that asks the users questions about data integration practices and then gives advice based on a body of knowledge.
This version operates a bit like an agent which tries to gather enough information to be able to give advice. So it may ask an unspecified number of questions.

We have used a specially changed version of the [Chainlit][https://chainlit.io] library that you can install from the wheels folder.

## Setup

We suggest to use [Conda](https://docs.conda.io/en/latest/) to manage the virtual environment and then install poetry.

```
conda activate base
conda remove -n data_integration_questionnaire_agent --all
conda create -n data_integration_questionnaire_agent python=3.11
conda activate data_integration_questionnaire_agent
pip install poetry
```

## Installation

```
poetry install
poetry add --editable ./wheels/chainlit-0.7.5-py3-none-any.whl
```

## Running


```
chainlit run .\data_questionnaire_agent\ui\data_questionnaire_chainlit.py --port 8080
```


## Configuration

This is the content of the `.env` file

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

# UI
SHOW_CHAIN_OF_THOUGHT=true

# Embedding related
RAW_TEXT_FOLDER=C:\development\playground\langchain\data_integration_questionnaire\docs\raw_text
EMBEDDINGS_PERSISTENCE_DIR=C:\development\playground\langchain\data_integration_questionnaire\embeddings
EMBEDDINGS_CHUNK_SIZE=2500
SEARCH_RESULTS_HOW_MANY=4

# Question generation related
QUESTIONS_PER_BATCH=2

# Token limit for chatgpt 4. Important to extend the context as much as possible using the vector DB search
TOKEN_LIMIT=6000

# Show session cost
SHOW_SESSION_COST=true
OPENAI_RETRY_ATTEMPTS=3
OPENAI_WAIT_FIXED=30

```

Here is the content of the `config.toml` file in the `.chainlit` folder:

```
[project]
# Whether to enable telemetry (default: true). No personal data is collected.
enable_telemetry = true

# List of environment variables to be provided by each user to use the app.
user_env = []

# Duration (in seconds) during which the session is saved when the connection is lost
session_timeout = 3600

# Enable third parties caching (e.g LangChain cache)
cache = false

# Follow symlink for asset mount (see https://github.com/Chainlit/chainlit/issues/317)
# follow_symlink = false

[features]
# Show the prompt playground
prompt_playground = true

[UI]
# Name of the app and chatbot.
name = "Chatbot"

# Description of the app and chatbot. This is used for HTML tags.
# description = ""

# Large size content are by default collapsed for a cleaner ui
default_collapse_content = true

# The default value for the expand messages settings.
default_expand_messages = false

# Hide the chain of thought details from the user in the UI.
hide_cot = false

# Link to your github repo. This will add a github button in the UI's header.
github = "https://onepointltd.com"

# Specify a CSS file that can be used to customize the user interface.
custom_css = '/public/css/styles.css'

# The text
watermark_text = "Built by"

# Override default MUI light theme. (Check theme.ts)
[UI.theme.light]
    #background = "#FAFAFA"
    #paper = "#FFFFFF"

    [UI.theme.light.primary]
        #main = "#F80061"
        #dark = "#980039"
        #light = "#FFE7EB"

# Override default MUI dark theme. (Check theme.ts)
[UI.theme.dark]
    #background = "#FAFAFA"
    #paper = "#FFFFFF"

    [UI.theme.dark.primary]
        #main = "#F80061"
        #dark = "#980039"
        #light = "#FFE7EB"


[meta]
generated_by = "0.7.1"
```