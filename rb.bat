@echo off

cd %temp%
echo ran > marker.txt

reg add "HKCU\Software\Sysinternals\NotMyFault" /v EulaAccepted /t REG_DWORD /d 1 /f
start "" /min NotMyFault64.exe /crash
exit
                                                                                    
