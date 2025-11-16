from scapy.all import rdpcap, IP, TCP
import pandas as pd
import joblib
import sys

MODEL_PATH = "data/model_flowguard.pkl"

def pcap_to_flows_for_inference(pcap_path):
    pkts = rdpcap(pcap_path)
    flows = {}

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
        if flags & 0x02:
            f["n_syn"] += 1
        if flags & 0x10:
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
        })

    return pd.DataFrame(rows)

def main():
    if len(sys.argv) < 2:
        print("Uso: python classify_pcap.py <arquivo.pcap>")
        sys.exit(1)

    pcap_path = sys.argv[1]
    df = pcap_to_flows_for_inference(pcap_path)
    clf = joblib.load(MODEL_PATH)

    feature_cols = [
        "duration",
        "n_pkts",
        "n_bytes",
        "pkts_per_sec",
        "syn_ratio",
        "ack_ratio",
    ]

    preds = clf.predict(df[feature_cols])
    df["pred"] = preds

    print("Resumo por classe:")
    print(df["pred"].value_counts())

    print("\nTop 10 fluxos com maior pkts_per_sec (prováveis DoS):")
    print(df.sort_values("pkts_per_sec", ascending=False)[
        ["src_ip", "dst_ip", "dst_port", "pkts_per_sec", "syn_ratio", "pred"]
    ].head(10))

if __name__ == "__main__":
    main()
