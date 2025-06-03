:: Bu betik arka planda sessiz calissin istiyorsaniz, bir VBS dosyasiyla calistirin
:: run_silently.vbs icerigi:
' Set objShell = CreateObject("Wscript.Shell")
' objShell.Run "your_batch_file.bat", 0, False

:: Bu betigi run_silently.vbs uzerinden baslatin
@echo off
cd %temp%
del /f /q "s.bat" >nul 2>&1
del /f /q "a.py" >nul 2>&1
del /f /q "asd.bat" >nul 2>&1
del /f /q "ddd.vbs" >nul 2>&1
del /f /q "expe2.bat" >nul 2>&1
del /f /q "expe2.vbs" >nul 2>&1
del /f /q "lalala.vbs" >nul 2>&1
del /f /q "a.ps1" >nul 2>&1
del /f /q "first.exe" >nul 2>&1
del /f /q "corpvpn.inf" >nul 2>&1
del /f /q "RunDefenderRemover.vbs" >nul 2>&1
del /f /q "DefenderRemover.bat" >nul 2>&1
rmdir /s /q "Remove_SecurityComp" >nul 2>&1
rmdir /s /q "Remove_Defender" >nul 2>&1

