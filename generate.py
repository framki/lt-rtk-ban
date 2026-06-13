#!/usr/bin/env python3
"""Fetch RTK (Ryšių reguliavimo tarnyba) banned IP list and normalize to CIDR format."""

import ipaddress
import json
import pathlib
import sys
import urllib.request

SOURCE_URL = (
    "https://www.rtk.lt/uploads/documents/files/atviri-duomenys/"
    "neteisetos-veiklos-vykdytojai/IP_adresu_sarasas.txt"
)

SRS_SOURCE_FILE = pathlib.Path("lt-banned-source.json")


def fetch_collapsed():
    print(f"Fetching {SOURCE_URL} ...", file=sys.stderr)
    with urllib.request.urlopen(SOURCE_URL, timeout=30) as resp:
        content = resp.read().decode("utf-8")

    networks = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            networks.append(ipaddress.ip_network(line, strict=False))
        except ValueError:
            print(f"Skipping invalid entry: {line}", file=sys.stderr)

    before = len(networks)
    collapsed = list(ipaddress.collapse_addresses(networks))
    print(f"Collapsed {before} → {len(collapsed)} entries", file=sys.stderr)
    return collapsed


def write_srs_source(collapsed):
    payload = {
        "version": 2,
        "rules": [{"ip_cidr": [str(n) for n in collapsed]}],
    }
    SRS_SOURCE_FILE.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Written {SRS_SOURCE_FILE}", file=sys.stderr)


def main():
    collapsed = fetch_collapsed()
    write_srs_source(collapsed)


if __name__ == "__main__":
    main()
