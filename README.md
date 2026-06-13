# lt-rtk-ban

IP addresses banned by the Lithuanian telecoms regulator
([RTK](https://www.rtk.lt/uploads/documents/files/atviri-duomenys/neteisetos-veiklos-vykdytojai/IP_adresu_sarasas.txt)),
collapsed into CIDR blocks and republished daily for [podkop](https://github.com/itdoginfo/podkop).

## Usage

Add this URL to podkop's remote subnet lists:

```
https://framki.github.io/lt-rtk-ban/lt-banned.lst
```

The file is plain text, one CIDR per line. Entry counts and the last update
time are on the [project page](https://framki.github.io/lt-rtk-ban/).
