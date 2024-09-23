# Phase One

Solved by: @0x251e

- Category: OSINT
- Description:

We had one of our agents infiltrate an adversary's lab and photograph a gateway device that can get us access to their network. We need to develop an exploit as soon as possible. Attached is a picture of the device. Get us intel on what MCU the device is utilizing so we can continue with our research. 

Flag format: pctf{mcu\_vendor\_name} (example: pctf{broadcom}

Challenge Image: 
![target\_product](target_product.jpg)

### Step 1: Google Dorking 
```
D-Link dsl-6300v intext:'Chip'
```

With this Google Search dorking, it will lead to the page where it contains specification information of the router 

### Step 2: Find the brand name for the mcu chip

From this [page](https://techinfodepot.shoutwiki.com/wiki/D-Link_DSL-6300V), it contains name of the brand which supplies the chip for the router

MCU Vendor Name: Ikanos

**Flag:** `pctf{ikanos}`




