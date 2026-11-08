# TraceForge

TraceForge is a beginner-friendly **offline PCAP analyzer**. It reads an existing packet-capture file and summarizes protocol counts, frequently seen IP addresses, and source/destination conversations.

It does **not** sniff live network traffic or send packets.

## Features

- Reads `.pcap` and `.pcapng` capture files using Scapy
- Counts TCP, UDP, DNS, other IP, and non-IP packets
- Lists the most frequently seen IP addresses
- Summarizes common source/destination conversations
- Prints readable output or JSON

## Requirements

- Python 3.10+
- Scapy

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Analyze a capture file:

```bash
python traceforge.py sample.pcap
```

Print JSON:

```bash
python traceforge.py sample.pcap --json
```

Use a capture file that you created yourself or one explicitly provided for training. If you do not have a PCAP yet, install Wireshark and create a short capture on your own device, or use an instructor-provided practice capture.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## How it works

1. Scapy reads the saved capture file.
2. TraceForge checks each packet for an IP layer.
3. It counts TCP, UDP, and DNS layers when present.
4. It records source/destination IP appearances and conversations.
5. It prints a summary or JSON report.

## Limitations

- This is a learning tool, not an intrusion detection system.
- It does not determine whether traffic is malicious.
- Host counts are packet appearances, not unique devices.
- It only summarizes IP-based packets for host and conversation counts.

## Responsible use

Analyze only packet captures you created yourself or are authorized to inspect. Captures can contain private information such as IP addresses, URLs, and unencrypted data. Do not publish sensitive captures or personal data.

## Learning goals

This project introduces PCAP files, packet layers, IP addresses, TCP/UDP, DNS, Python counters, third-party libraries, and JSON reports.
