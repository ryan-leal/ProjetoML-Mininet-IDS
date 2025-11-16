from scapy.all import rdpcap, IP, TCP
import pandas as pd

def pcap_to_flows(pcap_path, label):
    print(f"[+] Lendo {pcap_path} com label={label}...")
    pkts = rdpcap(pcap_path)

    flows = {}  # (src, dst, sport, dport) -> stats

    for pkt in pkts:
        if IP not in pkt or TCP not in pkt:
            continue

        ip = pkt[IP]
        tcp = pkt[TCP]

        src = ip.src
        dst = ip.dst
        sport = tcp.sport
        dport = tcp.dport
        t = float(pkt.time)
        length = len(pkt)
        flags = int(tcp.flags)

        key = (src, dst, sport, dport)

        if key not in flows:
            flows[key] = {
                "src_ip": src,
                "dst_ip": dst,
                "dst_port": dport,
                "start_time": t,
                "end_time": t,
                "n_pkts": 0,
                "n_bytes": 0,
                "n_syn": 0,
                "n_ack": 0,
            }

        f = flows[key]
        f["n_pkts"] += 1
        f["n_bytes"] += length
        f["end_time"] = t

        if flags & 0x02:  # SYN
            f["n_syn"] += 1
        if flags & 0x10:  # ACK
            f["n_ack"] += 1

    rows = []
    for _, f in flows.items():
        duration = max(f["end_time"] - f["start_time"], 1e-6)
        pkts_per_sec = f["n_pkts"] / duration
        syn_ratio = f["n_syn"] / max(f["n_pkts"], 1)
        ack_ratio = f["n_ack"] / max(f["n_pkts"], 1)

        rows.append({
            "src_ip": f["src_ip"],
            "dst_ip": f["dst_ip"],
            "dst_port": f["dst_port"],
            "duration": duration,
            "n_pkts": f["n_pkts"],
            "n_bytes": f["n_bytes"],
            "pkts_per_sec": pkts_per_sec,
            "syn_ratio": syn_ratio,
            "ack_ratio": ack_ratio,
            "label": label,
        })

    df = pd.DataFrame(rows)
    print(f"[+] {pcap_path}: {len(df)} fluxos gerados")
    return df


if __name__ == "__main__":
    normal_df = pcap_to_flows("./capture_results/captureNormal.pcap", label="normal")
    scan_df   = pcap_to_flows("./capture_results/captureScan.pcap",   label="scan")
    dos_df    = pcap_to_flows("./capture_results/captureDos.pcap",    label="dos")

    all_df = pd.concat([normal_df, scan_df, dos_df], ignore_index=True)

    all_df.to_csv("data/flows_features.csv", index=False)
    print(all_df.head())
    print(f"\n[+] Salvo em data/flows_features.csv com {len(all_df)} linhas.")
