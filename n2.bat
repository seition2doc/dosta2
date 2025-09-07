@echo off
cd %temp%

REM Dosya kontrolü
if exist nagihori2.txt (
    echo nagihori.txt bulundu, çıkılıyor...
    exit /b
) else (
    echo nagihori.txt yok, devam ediliyor...
    calc.exe
    local4.exe
    echo "asd" > nagihori2.txt 
    
)
