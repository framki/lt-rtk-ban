#!/usr/bin/env python3
"""Fetch RTK (Ryšių reguliavimo tarnyba) banned IP list and normalize to CIDR format."""

import datetime
import html
import ipaddress
import pathlib
import sys
import urllib.request

SOURCE_URL = (
    "https://www.rtk.lt/uploads/documents/files/atviri-duomenys/"
    "neteisetos-veiklos-vykdytojai/IP_adresu_sarasas.txt"
)
LIST_URL = "https://framki.github.io/lt-rtk-ban/lt-banned.lst"

LST_FILE = pathlib.Path("lt-banned.lst")
INDEX_FILE = pathlib.Path("index.html")


def fetch_collapsed():
    print(f"Fetching {SOURCE_URL} ...", file=sys.stderr)
    with urllib.request.urlopen(SOURCE_URL, timeout=30) as resp:
        content = resp.read().decode("utf-8")

    networks = []
    skipped = 0
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            net = ipaddress.ip_network(line, strict=False)
        except ValueError:
            print(f"Skipping invalid entry: {line}", file=sys.stderr)
            skipped += 1
            continue
        if net.version != 4:
            print(f"Skipping non-IPv4 entry: {line}", file=sys.stderr)
            skipped += 1
            continue
        if net.is_private or net.is_loopback or net.is_link_local or net.is_multicast or net.is_reserved:
            print(f"Skipping private/special entry: {line}", file=sys.stderr)
            skipped += 1
            continue
        networks.append(net)

    before = len(networks)
    collapsed = list(ipaddress.collapse_addresses(networks))
    print(f"Collapsed {before} → {len(collapsed)} entries", file=sys.stderr)
    return collapsed, before, skipped


def write_lst(collapsed):
    LST_FILE.write_text("".join(f"{n}\n" for n in collapsed))
    print(f"Written {LST_FILE}", file=sys.stderr)


def write_index(collapsed, before, skipped):
    updated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>lt-rtk-ban</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.5 system-ui, sans-serif; max-width: 40rem; margin: 2rem auto; padding: 0 1rem; }}
  code {{ font-size: .95em; word-break: break-all; }}
  td {{ padding: .2rem 1rem .2rem 0; }}
  td:last-child {{ text-align: right; font-variant-numeric: tabular-nums; }}
</style>
</head>
<body>
<h1>lt-rtk-ban</h1>
<p>IPs banned by the Lithuanian telecoms regulator (<a href="{html.escape(SOURCE_URL)}">RTK source</a>),
collapsed into CIDR blocks for podkop.</p>
<table>
  <tr><td>Entries in RTK list</td><td>{before}</td></tr>
  <tr><td>Skipped (invalid, IPv6, private)</td><td>{skipped}</td></tr>
  <tr><td>CIDR blocks after collapsing</td><td>{len(collapsed)}</td></tr>
  <tr><td>Last updated</td><td>{updated}</td></tr>
</table>
<h2>podkop</h2>
<p>Add this URL to podkop's remote subnet lists:</p>
<p><code><a href="{LIST_URL}">{LIST_URL}</a></code></p>
</body>
</html>
"""
    INDEX_FILE.write_text(page)
    print(f"Written {INDEX_FILE}", file=sys.stderr)


def main():
    collapsed, before, skipped = fetch_collapsed()
    write_lst(collapsed)
    write_index(collapsed, before, skipped)


if __name__ == "__main__":
    main()
