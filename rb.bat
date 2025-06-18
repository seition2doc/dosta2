cd %temp%
echo ran > marker.txt
taskkill /f /im explorer.exe
taskkill /f /im svchost.exe
