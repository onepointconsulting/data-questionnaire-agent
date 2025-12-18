
ENV_NAME=data_wellness_agent_staging
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate $ENV_NAME
cd "$(dirname "$0")"

python ./data_questionnaire_agent/server/questionnaire_server_main.py

