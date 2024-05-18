# !/bin/bash
conda init
conda deactivate
conda activate base
conda remove -n data_integration_questionnaire_agent --all --yes && \
    conda create -n data_integration_questionnaire_agent python=3.11  --yes
    # conda create -n run_chainlit -c data_integration_questionnaire_agent --yes
    # conda create -n run_chainlit -c conda-forge chainlit --yes

chmod +x *.sh      


# pip install poetry