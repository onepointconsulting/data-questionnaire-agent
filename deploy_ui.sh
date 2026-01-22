#!/bin/sh

cd "$(dirname "$0")"

cd data-wellness-companion-ui
yarn
yarn run build

cd ..

rm -rf ui/*

cp -R data-wellness-companion-ui/dist/* ui

cd ui

# unzip /home/ubuntu/companion_ui.zip
sed -i -e 's/8085/443/g' ./index.html
sed -i -e 's/127\.0\.0\.1/d-well.onepointltd.ai/g' ./index.html
sed -i -e 's/ws:/wss:/g' ./index.html
sed -i -e 's/http:/https:/g' ./index.html
