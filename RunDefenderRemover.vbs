Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "cmd.exe", "/c "DefenderRemover.bat"", "", "runas", 0
