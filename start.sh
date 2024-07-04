#!/bin/bash

# Activate environment
. venv/bin/activate;

# Install all libraries in the right environment
./venv/bin/poetry install

# Build the UI
echo Building the User Interface
poetry run build-ui

# Build the database if requested
echo Building database
python ./data_questionnaire_agent/bootstrap/sql_script.py ./sql/db_setup.sql

# Run the main application
/app/venv/bin/python ./data_questionnaire_agent/server/questionnaire_server_main.py
# /app/venv/bin/python ./data_questionnaire_agent/toml_support.py