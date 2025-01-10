#!/bin/sh
# Change the environment as needed.
ENV_NAME=data_wellness_agent_staging
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate $ENV_NAME
cd /home/ubuntu/projects/data-wellness-companion-staging

python ./data_questionnaire_agent/server/questionnaire_server_main.py

(base) ubuntu@ip-10-0-0-22:~/projects/data-wellness-companion-staging$ whereis sh
sh: /bin/sh /bin/sh.distrib /usr/share/man/man1/sh.1.gz
