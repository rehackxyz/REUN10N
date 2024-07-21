---
title: The Amazing CyberHunt Writeup
author: whymir
date: 2024-07-21 00:00:00
categories: [Forensics]
---

# The Amazing CyberHunt Writeup

This write-up documents our journey through The Amazing Cyber Hunt 2024 as team **RE:UN10N Jr**, comprising myself (whymir), Sara (ssi51), and Firdaus (vicevirus). We tackled various challenges with determination and teamwork.

Also available at https://whymir.github.io/posts/The-Amazing-CyberHunt-Writeup/

## Files

All challenge are given. Refer to this [link](https://pixeldrain.com/u/Cy7ZxjJa).
 
# Physical Challenge

As the competition started, we had 2 categories as mentioned before which were physical and digital competition. For the physical challenge, the organiser gave us a USB thumb drive. 

The USB thumb drive was empty when opened in Windows host, but if you open it in Ubuntu, it contains two files, `WPSetting.dat` and another file which I forgot the name. Sorry. 

This means, the USB could be corrupted or the file was deleted. To gain back what data or documents, I used *"Recuva"* to recover files. `Evidence3.wim` and `Evidence4.jpg.xz`.

## WAVing Flags

> It seems like people hide secret in all sort of files these days. If
> they cant see it, they cant hack it. Using the pendrive you received,
> locate a file named 'Evidence 3.jpg' and find the hidden flag inside.
> note: there is no header for this flag. enter the 'flags' directly
> without the UTAR{}

`Evidence3.wim` is Windows Imaging Format which means we can open or extract the data directly. I used file archiever to extract it. 
![image](https://hackmd.io/_uploads/r10Ahfqu0.png)

Started with a simple command such as file and `exiftools`. There was nothing fun. 
![image](https://hackmd.io/_uploads/Sk6N6fcuC.png)

Next, since this category belongs to Forensics Challenge, it might need some steganography techniques to be applied to this. To prove it, I used `binwalk`.

![image](https://hackmd.io/_uploads/H1eg0zc_C.png)

As shown in the screenshot, there was 7zip file embedded within this image. Even the extension was set as `.jpeg`, we still can extract it using `7z`.

![image](https://hackmd.io/_uploads/BkiVRzc_A.png)

We found a new file name, "secretmessage.pdf"

![image](https://hackmd.io/_uploads/S1MPRzc_R.png)

During solving this PDF challenge, I used `pdfid`,`pdfinfo` and `pdfparser`. A crucial hint given was about the challenge name and using `pdfparser`, I managed to capture some WAV headers.

![image](https://hackmd.io/_uploads/S14kkXcuR.png)

My teammate, Sara helped me at this stage and she managed to get the Wav file by using `foremost`.

![image](https://hackmd.io/_uploads/B14Ny7cOC.png)

We opened the file using Audacity and view its spectogram.
![image](https://hackmd.io/_uploads/S1Ed1mcu0.png)

>FLAG: UTAR{UNMASKING CYBER SECRET}

## GEOmancer
> Looking 'deep' at the pendrive you received, you should see a '******.xz' file.
>It was a picture I took during my cuti cuti Malaysia trip last month, but somehow i cant remember where it was. Can you help me find the city name?
>note: the flag is the city name, without the UTAR{} header.

We validate the file type of the `Evidence4.jpg.xz` file using `file` command. 
![image](https://hackmd.io/_uploads/r1fbxXcOC.png)

XZ compression can be extracted using 7z. 

![image](https://hackmd.io/_uploads/rJr4xXqOA.png)

We opened the image and as per the challenge name, it might be something related to OSINT
![image](https://hackmd.io/_uploads/r1xvlXqdR.png)

Since I have been visited this place before which TRX Exchange, I believed the flag was in Kuala Lumpur. Unfortunately it was wrong. I read again the challenge description, it mentioned something about "deep". That means there is something else in this image. Using `foremost`, I was able to extract the hidden files.

![image](https://hackmd.io/_uploads/B1pJb7qO0.png)

Notice that now we have four `.jpg` image files. One of the files was in full color as shown below: 

![image](https://hackmd.io/_uploads/ByLQWQ9OA.png)

I extracted the GPS in metadata using this [tools](https://tool.geoimgr.com/) to get the answer. 

![image](https://hackmd.io/_uploads/BJWT-75dA.png)

![image](https://hackmd.io/_uploads/rkERZX5dA.png)

>FLAG: Kota Bharu


# Digital Challenge

This challenge was hosted on their CTFd platform. 

## a Letter Please

>We found a zip file 'Evidence 2.zip', which we suspect to contain a hidden flag. Can you find it?
Flag format: UTAR{flags}

We tried to open the file, but it was not in zip format. 

![image](https://hackmd.io/_uploads/HkoJ7mcOC.png)

We validated the file type using `file` command. 

![image](https://hackmd.io/_uploads/ryK-QmcuC.png)

It was an EML file. FYI, this is an email format when we download through our email from any email platform.

The EML file can be opened using Thunderbird if there is only one file. However, the provided EML consisted of multiple EML files that can be combined into one file. One approach is by filtering the content-type. 

![image](https://hackmd.io/_uploads/S1KcNmqdA.png)

We observed that only the following content-type was different and had a document file attached.\
We moved to that line and got a brief information about the file. 
![image](https://hackmd.io/_uploads/SJ26VXcdA.png)

The challenge did mention about base64. We used this [link](https://base64.guru/converter/decode/file) to convert base64 to a file. 

Download the file and we got the flag. 
![image](https://hackmd.io/_uploads/SJuWSm9u0.png)
![image](https://hackmd.io/_uploads/H1uQHXcdC.png)

>FLAG:UTAR{InvisibleEvidenceSpeaks}

## bad http
>We have intercepted unsecure HTTP traffic from the network. The http.pcap file contains the traffic captured during a SQL injections conducted on a HTTP site. Analyze the pcap file to uncover the hidden flag. The flag is hashed using some common hash function.
Flag format: UTAR{your_flag_here}

This challenge can be done using two methods. 
1. Using `strings` command against the pcap file\
`strings http.pcap`

![image](https://hackmd.io/_uploads/Hk3B8Q9_R.png)

2. Analysing using Wireshark
This challenge was straight forward. It mentioned about SQL injection.

-- Follow the TCP stream
![image](https://hackmd.io/_uploads/Skc4v75u0.png)

Keep scrolling the stream until find the flag.
![image](https://hackmd.io/_uploads/ByPUwm5dR.png)

-- search frame contains "UTAR"
![image](https://hackmd.io/_uploads/HyaFw75dR.png)

Then follow the TCP stream or HTTP stream.

The flag was hashed so we need to crack it. We used this [tool](https://crackstation.net/) to crack.

![image](https://hackmd.io/_uploads/rktqUm9O0.png)


>FLAG: UTAR{Philosopher}

## Forensics 200
>Given a shell script file 'persistence.sh', find the flag.

We validated the file using `file`. 
![image](https://hackmd.io/_uploads/SyLyum5_R.png)

It had base64 encoded strings. We decoded the base64.

![image](https://hackmd.io/_uploads/BJfQ_Q5_R.png)

>FLAG: UTAR{9ce23f07e6b9bfc37508163b07e4d1b5}

## Hex is Fun
>here we go again... I found another file named 'Evidence 5.gif'. So i guess there is another flag inside. What is it?
Flag Format: UTAR{flags}

The file was a GiF file. I used `binwalk`

![image](https://hackmd.io/_uploads/rJjpdX5dC.png)

It had a secret file. Opened the file and got the flag.
![image](https://hackmd.io/_uploads/ByqJt7qdC.png)
> FLAG: UTAR{BitsNeverLie}


## Message in Picture
>One day, during a covert mission, Mrs Smith left a photo 'Evidence 1.jpeg' of their cute baby to Mr Smith, and then she disappeared. Is Mrs Smith trying to tell Mr Smith something? Could it be a flag?
Flag Format: UTAR{flags}

Given the file name as `Evidence 1`. I validated it using the `file` command. 
![image](https://hackmd.io/_uploads/SJ6VtQc_C.png)

It contained an embedded PPT file within this image. But, it missing some parts like "Content-Type.xml". It means something was hidden here. 

![image](https://hackmd.io/_uploads/ryeFKXc_C.png)

Again, I used `binwalk` to extract any file. 
![image](https://hackmd.io/_uploads/BJP0Ymqd0.png)

Now it had something that might be interesting. Look into all files.

![image](https://hackmd.io/_uploads/H1lO5X5_C.png)

Only this jpeg looked interesting to me. Since most challenges like to use `thumbnails.jpeg` as the flag. 
` open docProps/thumbnail.jpeg `

>FLAG: UTAR{DataRevealsAll}


## Unsolved Category
### Ole - Dirty Laundry
### Sus http
### Riddle is Fun

---
title: The Amazing CyberHunt Writeup
author: vicevirus
date: 2024-07-21 00:00:00
categories: [Binary Exploitation]
---

## Bin100

Decompile the provided file using `dnspy` too and found the seed defined as `123456`. Modify the code to loop through secret.

```
using System;
namespace UTAR_bin000
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            Console.WriteLine("Welcome to UTAR bin100");

            // Loop through the entire secret array
            for (int i = 0; i < Program.secret.Length; i++)
            {
                int num = Program.getSuperL33tNumber();

                int value = (int)(Program.secret[i] ^ (byte)num);
 
                Console.Write(Convert.ToChar(value));
            }

            Console.WriteLine();
        }

        private static int getUltraSuperL33tWatchaNumber()
        {
            return new Random().Next(1, 38);
        }

        private static int getSuperL33tNumber()
        {
            return Program.random.Next(1, 38);
        }

        private static Random random = new Random(123456);

        private static byte[] secret = new byte[]
        {
            95, 80, 67, 92, 100, 32, 58, 56, 116, 40, 103, 57, 37, 52, 47, 64,
            127, 45, 35, 48, 42, 99, 120, 71, 52, 104, 101, 99, 44, 118, 108, 36,
            71, 49, 19, 96, 120, 110
        };
    }
}
```

## Bin200

```
def xor_check():
    checks = [
        (0, 0x6B, 62),
        (1, 0x75, 33),
        (2, 0x65, 36),
        (3, 0x68, 58),
        (4, 0x78, 3),
        (37, 0x78, 5)
    ]
    
    flag = [''] * 38
    for index, xor_value, expected in checks:
        flag[index] = chr(expected ^ xor_value)
    
    stuff = [
        ord(c) for c in 'f17b245513f53cef837b54g9:7b2:99b'
    ]
    
    for i in range(32):
        flag[i + 5] = chr(stuff[i] - 1)
    
    return ''.join(flag)

if __name__ == "__main__":
    flag = xor_check()
    print(flag)
```
