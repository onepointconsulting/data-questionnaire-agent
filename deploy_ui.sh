#!/bin/bash

# Change the root folder as needed.
# The purpose of this script is to deploy the ui and configure it automatically.

cd ~/projects/data-wellness-companion-staging/ui
rm -rf *
unzip /home/ubuntu/companion_ui.zip
sed -i -e 's/8085/8083/g' ./index.html
sed -i -e 's/127\.0\.0\.1/176.34.128.143/g' ./index.html