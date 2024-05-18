
# SETUP

# . ./init.sh
# pipx install --suffix=@1.2.0 poetry==1.7.0
conda activate data_integration_questionnaire_agent

python3 -m pip install --user --upgrade pipx
conda install -c conda-forge pipx --yes
pipx ensurepath    

# pipx install --suffix=@1.8.2 poetry==1.8.2 --python $(which python)
pipx install poetry==1.8.2 --python $(which python)
# pipx reinstall poetry==1.8.2 --python $(which python)


poetry lock

# INSTALLATION
poetry install   && \
poetry add --editable ./wheels/chainlit-0.7.8.10-py3-none-any.whl

# pip install langchain-community faiss-cpu langchain-openai tiktoken  

# Installation
# fix the version of poetry pack
poetry install 

# Running

# PREPARE
# cp prompts_pt.toml
python ./data_questionnaire_agent/config.py
python ./data_questionnaire_agent/utils/tracker_db_init.py


# RUNNING


chainlit run ./data_questionnaire_agent/ui/data_questionnaire_chainlit.py --port 8080
