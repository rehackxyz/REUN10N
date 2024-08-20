# Recursion
Solved by **yappare**

## Question
I caught my co-worker moving some weird files on a USB, can you tell me whats going on?

## Solution
- Open the `usb.pcap.ng` using Wireshark and note it has an archive file in it.
- Use `binwalk` to grab the archived file, extract it. 
- Will receive another archive file.
- Repeat the steps until receive the final file, `layer1.pcapng`
- Sort the packets in the Wireshark according to its sizes, decode the one with the biggest size

![f](https://i.ibb.co/DfdSdCF/z.png)

### Flag
`crew{l00ks_l1ke_y0u_mad3_1t!}`
