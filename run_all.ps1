Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-File", ".\start.ps1"
Start-Process -FilePath "cmd" -ArgumentList "/k", "cd data-wellness-companion-ui && run_dev.bat"