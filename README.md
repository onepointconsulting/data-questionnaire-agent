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
conda remove -n data_integration_questionnaire_agent --all
conda create -n data_integration_questionnaire_agent python=3.11
conda activate data_integration_questionnaire_agent
pip install poetry
```

## Installation

```
poetry install
poetry add --editable ./wheels/chainlit-0.7.8.7-py3-none-any.whl
```

## Running


```
chainlit run .\data_questionnaire_agent\ui\data_questionnaire_chainlit.py --port 8080
```


## Configuration

This is the content of the `.env` file

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

## Note on sqllite3 on Windows

If you have a hard time installing sqllite3 on Windows follow these instructions:

https://zeljic.com/blog/sqlite-lib-windows-10/

1. Download source from [source](https://www.sqlite.org/download.html)

	For example: [source](https://www.sqlite.org/2023/sqlite-amalgamation-3430100.zip) `https://www.sqlite.org/2023/sqlite-amalgamation-3430100.zip`
2. Download binary from [binary](https://www.sqlite.org/download.html)

	For example: [binary](https://www.sqlite.org/2023/sqlite-dll-win64-x64-3430100.zip) `https://www.sqlite.org/2023/sqlite-dll-win64-x64-3430100.zip`
    
3. Extract both archives to the same directory
    
4. Open **Developer Command Prompt for VS 2017** by typing *Developer Command* in Windows Search

5. Go to directory where you've extracted **source code** and **binary** files (via opened cmd)
6. Run 
	```lib /DEF:sqlite3.def /OUT:sqlite3.lib /MACHINE:x64```
7. Copy all of the files including `sqlite3.h` into one of the include folders used by `cl.exe` like e.g. `-IC:\Users\gilfe\miniconda3\envs\data_integration_questionnaire_agent\Include`
	
[Blog post](https://zeljic.com/blog/sqlite-lib-windows-10/)