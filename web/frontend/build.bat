SET BUILD_NAME=companion_ui.zip
REM Just in case the UI folder exists on your computer
SET UI_FOLDER=C:\development\playground\langchain\data_questionnaire_agent\ui

call yarn run build

cd dist

powershell Compress-Archive -Force * ..\%BUILD_NAME%
cd ..
xcopy dist\* %UI_FOLDER% /e/s