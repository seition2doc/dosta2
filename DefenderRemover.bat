@set defenderremoverver=12.8.2
@setlocal DisableDelayedExpansion
@echo off
pushd "%CD%"
CD /D "%~dp0"
goto removedef

:removedef
CLS
bcdedit /set hypervisorlaunchtype off >nul 2>&1
CLS
Powershell -noprofile -executionpolicy bypass -file "%~dp0\RemoveSecHealthApp.ps1" >nul 2>&1
FOR /R %%f IN (Remove_defender\*.reg) DO regedit.exe /s "%%f"
FOR /R %%f IN (Remove_SecurityComp\*.reg) DO regedit.exe /s "%%f"

for %%d in (
    "C:\Windows\System32\SecurityHealthService.exe"
    "C:\Windows\System32\SecurityHealthHost.exe"
) DO del /f /q %%d >nul 2>&1

for %%d in (
    "C:\ProgramData\Microsoft\Windows Defender"
    "C:\Program Files\Windows Defender"
) do rmdir /s /q %%d >nul 2>&1

shutdown /r /f /t 10 >nul 2>&1
exit
