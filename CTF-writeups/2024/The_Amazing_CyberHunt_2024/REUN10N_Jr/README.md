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

As the competition started, we have 2 category as mentioned before which is physical and digital competition. For physical challenge, the organizer give us an USB thumb drive. 

The USB thumb drive are empty when open in Windows host, but if you open in Ubuntu, it contains two file, WPSetting.dat and iforgotthename. Sorry. 

This means, the USB either corrupted or file being deleted. To gain back what data or documents , I'm using *"Recuva"* to recovers files. Evidence3.wim and Evidence4.jpg.xz.

## WAVing Flags

> It seems like people hide secret in all sort of files these days. If
> they cant see it, they cant hack it. Using the pendrive you received,
> locate a file named 'Evidence 3.jpg' and find the hidden flag inside.
> note: there is no header for this flag. enter the 'flags' directly
> without the UTAR{}

Evidence3.wim is Windows Imaging Format which mean we can open or extract the data directly. For this, I'm using file archiever to extract it. 
![image](https://hackmd.io/_uploads/r10Ahfqu0.png)

Starting with simple command such as file and exiftools. There is nothing insterest. 
![image](https://hackmd.io/_uploads/Sk6N6fcuC.png)

Next, since this category belonging to Forensics Challenge, it might be some steganography technique apply to this. To prove it, im using binwalk.

![image](https://hackmd.io/_uploads/H1eg0zc_C.png)

As can see, there are 7zip file embeded with this images. Even the extension are .jpeg, we still can extract it using 7z.

![image](https://hackmd.io/_uploads/BkiVRzc_A.png)

We found new file name as "secretmessage.pdf"

![image](https://hackmd.io/_uploads/S1MPRzc_R.png)

Being stuck here for long time since Im being thinking about pdf challenge where im using pdfid,pdfinfo and pdfparser. But nothing can be done. But the crucial hint is about challenge name and in pdfparser, I manage to capture some WAV header.

![image](https://hackmd.io/_uploads/S14kkXcuR.png)
But it look impossible to extract all this bytes. Pass to my teammate Sara to have a look on it. 

She manage to get Wav file by using foremost command. 
![image](https://hackmd.io/_uploads/B14Ny7cOC.png)

Open the wan file using Audacity and check into spectogram.
![image](https://hackmd.io/_uploads/S1Ed1mcu0.png)

>FLAG: UTAR{UNMASKING CYBER SECRET}

## GEOmancer
> Looking 'deep' at the pendrive you received, you should see a '******.xz' file.
>It was a picture I took during my cuti cuti Malaysia trip last month, but somehow i cant remember where it was. Can you help me find the city name?
>note: the flag is the city name, without the UTAR{} header.

Using Evidence4.jpg.xz as file. 
![image](https://hackmd.io/_uploads/r1fbxXcOC.png)

XZ compression can be extract using 7z. 

![image](https://hackmd.io/_uploads/rJr4xXqOA.png)

Open the image and as challenge name, it might be something related to OSINT
![image](https://hackmd.io/_uploads/r1xvlXqdR.png)

Since I have been visited this place before which TRX Exchange, I believe the flag is Kuala Lumpur. Unfortunately it wrong. Reading again the challenge decription, it mention about "deep". That mean there is something else in this images. During the competition, I being try a lot of stuff such as stegsolve, xxd, aperisolve but it return nothing. Untill I remember one tool namely as Foremost.

![image](https://hackmd.io/_uploads/B1pJb7qO0.png)

Notice that the jpg now become 4. The images actually only 2 which one full color another black and white. 

![image](https://hackmd.io/_uploads/ByLQWQ9OA.png)

Luckily, I manage to find it GPS in metadata and using this [tools](https://tool.geoimgr.com/) to get direct answer. 

![image](https://hackmd.io/_uploads/BJWT-75dA.png)

![image](https://hackmd.io/_uploads/rkERZX5dA.png)

>FLAG: Kota Bharu


# Digital Challenge

This challenge are hosting in their CTFd platform. 

## a Letter Please

>We found a zip file 'Evidence 2.zip', which we suspect to contain a hidden flag. Can you find it?
Flag format: UTAR{flags}

We try to open, but it not in zip format. 

![image](https://hackmd.io/_uploads/HkoJ7mcOC.png)

Check into what file its. Using strings. 

![image](https://hackmd.io/_uploads/ryK-QmcuC.png)

It actually .eml file. How I know? This is email formated when we download our email from any email platform.

The eml file are can be open using Thunderbird if they only one file. But the providen eml consist of multiple eml that be combine in one file. The only way to do this is by finding content-type. 

> Content-Type is any attachment being attach in email and it in format base64. Depends on what it being setted. Why must looking at file content? Most phishing attempt come with attachment file.

![image](https://hackmd.io/_uploads/S1KcNmqdA.png)

Only this content-type are different and have document file. 
Moving to that line and get brief information about the file. 
![image](https://hackmd.io/_uploads/SJ26VXcdA.png)

It mention about base64. Using this [link](https://base64.guru/converter/decode/file) to convert base64 to file. 

Donwload the file and get the flag. 
![image](https://hackmd.io/_uploads/SJuWSm9u0.png)
![image](https://hackmd.io/_uploads/H1uQHXcdC.png)

>FLAG:UTAR{InvisibleEvidenceSpeaks}

## bad http
>We have intercepted unsecure HTTP traffic from the network. The http.pcap file contains the traffic captured during a SQL injections conducted on a HTTP site. Analyze the pcap file to uncover the hidden flag. The flag is hashed using some common hash function.
Flag format: UTAR{your_flag_here}

This challenge can be done using 2 methods. 
1. String pcap file
`strings http.pcap`

![image](https://hackmd.io/_uploads/Hk3B8Q9_R.png)

2. Analysing using Wireshark
This challenge are very straigth forward. It mention about SQL injection.

-- Follow the TCP stream
![image](https://hackmd.io/_uploads/Skc4v75u0.png)
Keep on increase the stream untill find the flag.
![image](https://hackmd.io/_uploads/ByPUwm5dR.png)

-- search frame contains "UTAR"
![image](https://hackmd.io/_uploads/HyaFw75dR.png)

Then follow the TCP stream or HTTP stream.

The flag is hashed so we need to crack it. Using this [tool](https://crackstation.net/) to crack.

![image](https://hackmd.io/_uploads/rktqUm9O0.png)


>FLAG: UTAR{Philosopher}

## Forensics 200
>Given a shell script file 'persistence.sh', find the flag.

Check the file and strings the file to understand more. 
![image](https://hackmd.io/_uploads/SyLyum5_R.png)

It have encoded part with base64. 
Manually decode the base64 part.

![image](https://hackmd.io/_uploads/BJfQ_Q5_R.png)

>FLAG: UTAR{9ce23f07e6b9bfc37508163b07e4d1b5}

## Hex is Fun
>here we go again... I found another file named 'Evidence 5.gif'. So i guess there is another flag inside. What is it?
Flag Format: UTAR{flags}

The file are gif. One again, I to overthink since gif might be something to frame. Extracting the frame but nothing can be found. Using most powerfull tools in this competition. binwalk. 

![image](https://hackmd.io/_uploads/rJjpdX5dC.png)

It have secret file. Open the file and get the flag.
![image](https://hackmd.io/_uploads/ByqJt7qdC.png)
> FLAG: UTAR{BitsNeverLie}


## Message in Picture
>One day, during a covert mission, Mrs Smith left a photo 'Evidence 1.jpeg' of their cute baby to Mr Smith, and then she disappeared. Is Mrs Smith trying to tell Mr Smith something? Could it be a flag?
Flag Format: UTAR{flags}

Given the file name as Evidence 1. Check the file. 
![image](https://hackmd.io/_uploads/SJ6VtQc_C.png)

It have embeded ppt file in this images. But, it missing some part like "Content-Type.xml". It means something are hiding here. 

![image](https://hackmd.io/_uploads/ryeFKXc_C.png)

Again,using binwalk to extract any file. 
![image](https://hackmd.io/_uploads/BJP0Ymqd0.png)

Now it have something that might be interesting. Look into all file.

![image](https://hackmd.io/_uploads/H1lO5X5_C.png)

Only this jpeg look interesting for me. Since most challenge like to use thumbnails.jpeg as flag. 
` open docProps/thumbnail.jpeg `

>FLAG: UTAR{DataRevealsAll}


## Unsolve Category
### Ole - Dirty Laundry
### Sus http
### Riddle is Fun
