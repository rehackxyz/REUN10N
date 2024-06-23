# Forensic - _wanna_be_a_streamer
Solved by **warlocksmurf** and **yappare**
Original writeup by **warlocksmurf** - https://warlocksmurf.github.io/posts/wanictf2024/

## Question
Sorry Mom, I'll work as a streamer.\
Watch my stream once in a while.\
(H.264 is used for video encoding.)

## Solution
Extract the RTP/RTSP packets from the given `.pcap` file and and use `h264` protocol using Wireshark.
`Edit->Preferences->Protocols->H264`

Once extracted, play the file using `ffmpeg` or other media player that supports the protocol, example IINA for MacOS.

### Flag
`FLAG{Th4nk_y0u_f0r_W4tching}``
