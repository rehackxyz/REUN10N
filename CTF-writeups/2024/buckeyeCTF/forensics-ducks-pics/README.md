# duck-pics

Solved by: @yappare

### Question
got a capture on the chall author while engaging in "personal matters". see what you can find.

### Solution:

1. Extract the keyboard strokes input from the pcap file 

```bash
tshark -r capture.pcapng -Y 'usb.src=="1.1.1"' -T fields -e usbhid.data |sed 's/../:&/g2' > dump
```

Based on the pcap, the USB source address 1.1.1 which transfer data to the host. It extracts raw HID data into a proper format to be convert into plaintext later. [References](https://wiki.osdev.org/USB_Human_Interface_Devices#USB_keyboard)

2. Parse the extracted usb hid data into readable format

With this [source code](https://raw.githubusercontent.com/TeamRocketIst/ctf-usb-keyboard-parser/refs/heads/master/usbkeyboard.py), we able to convert it to plaintext.

```bash
$ python3 usbkeyboard.py dump | grep bctf
bctf{SSteASt0p_s3nd1Ng_m3_DuCK_p1c$}
```

**Flag:** `bctf{SSteASt0p_s3nd1Ng_m3_DuCK_p1c$}`

