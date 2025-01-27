Set WshShell = CreateObject("WScript.Shell")
WshShell.Run Chr(34) & CreateObject("WScript.Shell").ExpandEnvironmentStrings("%temp%") & "\asd.bat" & Chr(34), 0
Set WshShell = Nothing