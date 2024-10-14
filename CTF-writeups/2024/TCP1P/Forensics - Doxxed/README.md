# Doxxed

Solved by: @Cookies to SELL and @yappare

## Question:
I recently forked a public repository on GitHub. After a few days I deleted my repo. However, my friend informed me that he are still able to access one of my commits from that fork which commit 4bxxxxx. Can you figure out how this happened? See the public repo below.

## Solution:
1. @Cookies to SELL found the docker image `53buahapel/sup3rsecretools`
2. @yappare continued 
3. `docker pull` from https://hub.docker.com/r/53buahapel/sup3rsecretools/tags
4. Then run into the docker images to confirm the file `exec` from `/usr/bin/exec` which is missing from the repo we downloaded from the CTF challenge.
5. Use `docker copy` to copy out the `exec` file from the docker image, then `strings exec`
6. Found weird Base64 alike 
```
VENQMVB7H
ODNmZTAzH
NGIyY2ZiH
MDlkZWFmH
YmI5NTViH
MDMzOTJhH
MDgzZDhmH
ODNiMn0KH
```
7. Removed all `H`, decode it.

**Flag:** `TCP1P{83fe034b2cfb09deafbb955b03392a083d8f83b2}`
