#!/usr/bin/env python3
"""TraceForge: beginner-friendly offline PCAP summary tool."""
import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from scapy.all import rdpcap, IP, TCP, UDP, DNS
except ImportError:
    rdpcap = None
    IP = TCP = UDP = DNS = None

def analyze_pcap(path):
    """Read a PCAP file and return simple protocol and host summaries."""
    if rdpcap is None:
        raise RuntimeError("Scapy is not installed. Run: python -m pip install -r requirements.txt")
    packets = rdpcap(str(path))
    protocols = Counter()
    hosts = Counter()
    conversations = Counter()

    for packet in packets:
        if IP in packet:
            src = packet[IP].src
            dst = packet[IP].dst
            hosts[src] += 1
            hosts[dst] += 1
            conversations[(src, dst)] += 1

            if TCP in packet:
                protocols["TCP"] += 1
            elif UDP in packet:
                protocols["UDP"] += 1
            else:
                protocols["Other IP"] += 1

            if DNS in packet:
                protocols["DNS"] += 1
        else:
            protocols["Non-IP"] += 1

    return {
        "file": Path(path).name,
        "total_packets": len(packets),
        "protocol_counts": dict(protocols.most_common()),
        "top_hosts": [
            {"ip": ip, "packet_appearances": count}
            for ip, count in hosts.most_common(10)
        ],
        "top_conversations": [
            {"source": src, "destination": dst, "packets": count}
            for (src, dst), count in conversations.most_common(10)
        ],
    }

def main():
    parser = argparse.ArgumentParser(
        description="Summarize an existing PCAP file offline. Does not capture live traffic."
    )
    parser.add_argument("pcap", help="Path to a .pcap or .pcapng capture file")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    path = Path(args.pcap)
    if not path.is_file():
        parser.error(f"File not found: {path}")

    try:
        report = analyze_pcap(path)
    except (RuntimeError, OSError, ValueError) as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"TraceForge report: {report['file']}")
    print(f"Total packets: {report['total_packets']}")
    print("\nProtocol counts:")
    for protocol, count in report["protocol_counts"].items():
        print(f"  {protocol:<12} {count}")
    print("\nTop hosts:")
    for host in report["top_hosts"]:
        print(f"  {host['ip']:<18} {host['packet_appearances']} appearances")
    print("\nTop conversations:")
    for item in report["top_conversations"]:
        print(f"  {item['source']} -> {item['destination']}: {item['packets']} packets")

if __name__ == "__main__":
    main()
