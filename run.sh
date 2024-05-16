
# SETUP

conda activate base
conda remove -n data_integration_questionnaire_agent --all
conda create -n data_integration_questionnaire_agent python=3.11 --yes
conda activate data_integration_questionnaire_agent
pip install poetry



# Installation

poetry install
poetry add --editable ./wheels/chainlit-0.7.8.10-py3-none-any.whl


# Running

# PREPARE
python ./data_questionnaire_agent/utils/tracker_db_init.py

# RUNNING


chainlit run ./data_questionnaire_agent/ui/data_questionnaire_chainlit.py --port 8080
