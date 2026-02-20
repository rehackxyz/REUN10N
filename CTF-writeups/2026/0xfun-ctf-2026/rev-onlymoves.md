# rev - Only Moves

The binary compares a 28-byte embedded target at `0x8057010` against a 28-byte computed value left on the stack (observed at `0x8600158`) right before it prints "Wrong!\n".
Instead of reversing the mov-fuscated VM, use an oracle: on the Wrong path, dump both exp and got.
By flipping one input byte at a time and looking at got_ref XOR got_mod, you can empirically see a triangular “suffix-only” effect (the change becomes a constant byte repeated from an index start = i ^ 1 to the end), which is easy to invert with queries.

 Files Needed:
`only_moves` (challenge binary)
`hook_printf.c` (`LD_PRELOAD` oracle shim source)
`hook_oracle.so` (compiled oracle shim; can be rebuilt from `hook_printf.c`)
`solve.py` (solver that queries the oracle and reconstructs the flag)
 
```c
typedef unsigned int u32;
typedef unsigned int usize;

typedef struct { char *p; usize cap; usize len; } buf_t;

static void sys_write(int fd, const void *p, usize n){
    unsigned int eax=4; // __NR_write
    unsigned int ebx=(unsigned int)fd;
    unsigned int ecx=(unsigned int)p;
    unsigned int edx=(unsigned int)n;
    __asm__ __volatile__("int $0x80" : "+a"(eax) : "b"(ebx), "c"(ecx), "d"(edx) : "memory");
}

static usize cstr_len(const char *s){
    usize n=0;
    while (s && s[n]) n++;
    return n;
}

static void bputc(buf_t *b, char c){ if (b->len < b->cap) b->p[b->len++] = c; }
static void bputs(buf_t *b, const char *s){ for (; *s; s++) bputc(b, *s); }
static void bput_hex32(buf_t *b, u32 v){
    static const char *hex="0123456789abcdef";
    for (int i=7;i>=0;i--) bputc(b, hex[(v>>(i*4))&0xF]);
}

static void bput_hex8(buf_t *b, unsigned char v){
    static const char *hex="0123456789abcdef";
    bputc(b, hex[(v >> 4) & 0xF]);
    bputc(b, hex[v & 0xF]);
}

int printf(const char *fmt, ...){
    // Intercept the specific messages used by the crackme.
    volatile u32 *p7070 = (u32*)0x8057070;
    volatile u32 *p7074 = (u32*)0x8057074;
    volatile u32 *p7078 = (u32*)0x8057078;
    volatile u32 *p707c = (u32*)0x805707c;

    // If this is the Wrong! print, dump a compact oracle line to stderr.
    // Compare by content to avoid relying on fixed addresses.
    if (fmt && fmt[0]=='W' && fmt[1]=='r' && fmt[2]=='o' && fmt[3]=='n' && fmt[4]=='g') {
        // Expected digest bytes live in .data at 0x8057010 (28 bytes).
        // Computed digest bytes appear to be placed on the fixed stack at 0x8600158 (28 bytes).
        volatile unsigned char *expected = (unsigned char*)0x8057010;
        volatile unsigned char *computed = (unsigned char*)0x8600158;

        unsigned int mismatch = 28;
        for (unsigned int i = 0; i < 28; i++) {
            if (expected[i] != computed[i]) { mismatch = i; break; }
        }

        char out[1024];
        buf_t b = { out, sizeof(out), 0 };
        bputs(&b, "[oracle] m="); bput_hex32(&b, mismatch);
        bputs(&b, " exp="); // expected 28 bytes
        for (unsigned int i = 0; i < 28; i++) bput_hex8(&b, expected[i]);
        bputs(&b, " got=");
        for (unsigned int i = 0; i < 28; i++) bput_hex8(&b, computed[i]);
        bputs(&b, " 7070="); bput_hex32(&b, *p7070);
        bputs(&b, " 7074="); bput_hex32(&b, *p7074);
        bputs(&b, " 7078="); bput_hex32(&b, *p7078);
        bputs(&b, " 707c="); bput_hex32(&b, *p707c);
        bputc(&b, '\n');
        sys_write(2, out, b.len);
    }

    usize n = cstr_len(fmt);
    if (n) sys_write(1, fmt, n);
    return (int)n;
}
Build the oracle shim (prints exp/got when program prints "Wrong!")
gcc -m32 -shared -fPIC -nostdlib -O2 -o hook_oracle.so hook_printf.c
```

FLAG:`0xfun{m0v_1s_tur1ng_c0mpl3t}`

## Attachments

- [script.py](https://raw.githubusercontent.com/rehackxyz/REUN10N/main/CTF-writeups/2026/0xfun-ctf-2026/assets/onlymoves-script.py)


Solved by: ha1qal
