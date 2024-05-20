#!/bin/bash

# Activate environment
. venv/bin/activate;

# Install all libraries in the right environment
./venv/bin/poetry install

# Build the UI
poetry run build-ui

# Run the main application
/app/venv/bin/python ./data_questionnaire_agent/server/questionnaire_server_main.py
# /app/venv/bin/python ./data_questionnaire_agent/toml_support.py