import os
import subprocess

# Temp klasörünü al
temp_dir = os.environ.get("TEMP")

# Dosya yolları
loa_py_path = os.path.join(temp_dir, "loa.py")
loa_bat_path = os.path.join(temp_dir, "loa.bat")
loa_vbs_path = os.path.join(temp_dir, "loa.vbs")

# Dosya içerikleri
loa_py_content = '''import os
os.system("calc.exe")
'''

loa_bat_content = f'''python "{loa_py_path}"
'''

loa_vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run Chr(34) & CreateObject("WScript.Shell").ExpandEnvironmentStrings("%temp%") & "\\loa.bat" & Chr(34), 0
Set WshShell = Nothing
'''

# Dosyaları yaz
with open(loa_py_path, "w") as f:
    f.write(loa_py_content)

with open(loa_bat_path, "w") as f:
    f.write(loa_bat_content)

with open(loa_vbs_path, "w") as f:
    f.write(loa_vbs_content)

# VBS scriptini çalıştır (arka planda)
subprocess.Popen(["wscript", loa_vbs_path], shell=True)
