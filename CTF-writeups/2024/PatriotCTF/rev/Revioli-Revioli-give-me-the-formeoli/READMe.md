# Revioli, Revioli, give me the formeoli

Solved by: @0x251e

- Category: Reverse
- Description:

Can you unlock the secret formula?

- Challenge File: revioli

### Step 1: Run the binary file

```
$ ./revioli
Enter-a the password-a:
```
crackme style challenge, have to analyze what is going on underneath

### Step 2: Use a decompiler to under the main function

```c
v7 = __readfsqword(0x28u);
  gen_correct_flag(s2, argv, envp);
  assemble_flag(s2, v6);
  printf("Enter-a the password-a: ");
  fgets(s, 256, _bss_start);
  s[strcspn(s, "\n")] = 0;
  if ( !strcmp(s, s2) )
    printf("Congratulations! The flag is: %s\n", v6);
  else
    puts("No toucha my spaget!");
  return 0;
}
```
We can observe the function of `gen_correct_flag` and `assemble_flag` is doing most of the heavy-lifting and will get the flag at the variable `v6`.

### Step 3: Analyze gen\_correct\_flag()

There are two code block that generate the flag

```
 v38 = __readfsqword(0x28u);
  for ( i = 0; i <= 14; ++i )
    v4[i] = calc((unsigned int)i);
  *(_QWORD *)dest = 0LL;
```

This part it has `calc` to perform calculation of Fibbonacci from 0 to 14.

```
 for ( j = 0; j <= 14; ++j )
  {
    snprintf(s, 0x14uLL, "%llu", v4[j]);
    strcat(dest, s);
  }
  snprintf(a1, 0x100uLL, "ITALY_%s", dest);
  return v38 - __readfsqword(0x28u);

```

This part it combine the fibbonacci number with `ITALY_`


### Step 4: Analyze assemble\_flag function: 

```
{
    return snprintf(a2, 0x100uLL, "PCTF{%s}", a1);
}
```

This part it combine the flag and flag header. 

### Step 5: Generate a script to calculate Fibbonacci Numbers

```py
a,b=0,1
fibb=str(a)
for _ in range(14):
    fibb+=str(b)
    a,b=b,a+b
print(fibb)
```

### Step 6: Merge the pieces together and you will get the flag

```sh
$ ./revioli
Enter-a the password-a: ITALY_01123581321345589144233377
Congratulations! The flag is: PCTF{ITALY_01123581321345589144233377}
```

**Flag:** `PCTF{out_0f_0ffic3_out_0f_M1nd}`


