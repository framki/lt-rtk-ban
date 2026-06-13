# lt-rtk-ban

Block IPs banned by the Lithuanian telecoms regulator ([RTK](https://www.rtk.lt/uploads/documents/files/atviri-duomenys/neteisetos-veiklos-vykdytojai/IP_adresu_sarasas.txt)), auto-updated daily as a sing-box rule-set.

## Usage

### podkop

Add the URL in podkop's custom list settings:

```
https://github.com/framki/lt-rtk-ban/releases/latest/download/lt-banned.srs
```

### sing-box

```json
{
  "tag": "lt-rtk-ban",
  "type": "remote",
  "format": "binary",
  "url": "https://github.com/framki/lt-rtk-ban/releases/latest/download/lt-banned.srs",
  "update_interval": "24h"
}
```

Reference it in a rule:

```json
{
  "rule_set": "lt-rtk-ban",
  "outbound": "block"
}
```
