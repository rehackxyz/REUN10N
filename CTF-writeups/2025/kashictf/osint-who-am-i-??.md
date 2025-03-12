# Who am I ??

Solved by: @0x251e

### Question
You've stumbled upon a bustling street with political posters. Find out after which politician this road is named. Flag Format: `KashiCTF{Full_Name}`

**Flag format clarification:** The full name is in `Title_Case`, without any diacritics, with each "special character (anything other than a-zA-Z)" replaced by an underscore.

Challenge Image:
![osint-1.png](REUN10N/CTF-writeups/2025/kashictf/osint-1.png)

### Solution:
1. Find text on the image as hint where you will find it is based in Hungary
2. Based on the email address on the blue banner, you will find it to this location at [Google Maps](https://www.google.com/maps/place/Duna+House+-+Damjanich+street/@47.503271,19.0550654,3a,60y,59.94h,82.87t/data=!3m7!1e1!3m5!1sLZ94gw-xDuWHyvxBQvjc7g!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D7.125217194973956%26panoid%3DLZ94gw-xDuWHyvxBQvjc7g%26yaw%3D59.93853930412397!7i16384!8i8192!4m14!1m7!3m6!1s0x4741dc7b992e0fad:0x7b74e942eed5913a!2sDuna+House+-+Damjanich+street!8m2!3d47.503281!4d19.055284!16s%2Fg%2F1tgnkvvh!3m5!1s0x4741dc7b992e0fad:0x7b74e942eed5913a!8m2!3d47.503281!4d19.055284!16s%2Fg%2F1tgnkvvh?entry=ttu&g_ep=EgoyMDI1MDIxOS4xIKXMDSoASAFQAw%3D%3D)

![osint-2.png](REUN10N/CTF-writeups/2025/kashictf/osint-2.png)
1. Finding out the full name of the politician based on the street can be found in [wikipedia](https://en.wikipedia.org/wiki/Endre_Bajcsy-Zsilinszky)

**Flag:**`KashiCTF{Endre_Bajcsy_Zsilinszky}`
