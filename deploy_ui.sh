cd ~/projects/data-wellness-companion-staging/ui
rm -rf *
unzip /home/ubuntu/companion_ui.zip
sed -i -e 's/8085/443/g' ./index.html
sed -i -e 's/127\.0\.0\.1/staging-d-well.onepointltd.ai/g' ./index.html
sed -i -e 's/ws:/wss:/g' ./index.html
sed -i -e 's/http:/https:/g' ./index.html
