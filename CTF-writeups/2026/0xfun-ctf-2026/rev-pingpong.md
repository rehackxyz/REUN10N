# rev - pingpong

```
char a0149545b5f4b5d[74] = "0149545b5f4b5d1e5c545d1a55036c5700404b46505d426e02001b4909030957414a7b7a48"; // weak
char aInvalidHexStri[18] = "Invalid hex string"; // weak
char a112105110103[15] = "112.105.110.103"; // weak
char a112111110103[15] = "112.111.110.103"; // weak
```

got XOR calculation by part. 2 key which is the ip itself. cut first half ip and another ip. xor

`0149545b5f4b5d1e5c545d1a55036c5700404b46505d426e02001b4909030957414a7b7a48`

XOR:
112.105.110.103
112.111.110.103

Flag: `0xfun{h0mem4d3_f1rewall_305x908fsdJJ}`

Solved by OS1RIS

Solved by: ha1qal
