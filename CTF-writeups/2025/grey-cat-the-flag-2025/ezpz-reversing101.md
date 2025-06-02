Solution
``` nc challs.nusgreyhats.org 33000
╔══════════════════════════════════════════════════════════════╗
║              REVERSE ENGINEERING QUIZ CHALLENGE              ║
╚══════════════════════════════════════════════════════════════╝
Answer all questions correctly to reveal the flag!
─────────────────────────────────────────────────────────────────

Question 1: What is the address of the main function in hex (i.e. 0x1234)?
Answer: 0x402db6
✓ Correct!

Question 2: What is the name of the libc function that has the same effect as function a?
Hint: We can try dis-assembling or de-compiling the program to understand what the function is doing.
Answer: strlen
✓ Correct!

Question 3: What is the length of the correct password?
Answer: 15
✓ Correct!

Question 4: Function b returns a constant value that is later used to check the password. What is the value returned by the function?
Hint: If a function is too complex, we can use a debugger to analyze the values at runtime! Note that the return value is typically stored in the RAX register at the end of a function.
Answer: 13969625720425389615
✓ Correct!

Question 5: Function c implements a popular encryption algorithm. What is this algorithm?
Hint: Google or even ChatGPT is your best friend.
Answer: RC4
✓ Correct!

Question 6: Finally, what is the correct password for this program?
Answer: honk-mimimimimi
✓ Correct!
```

Flag: grey{solv3d_m1_f1r5t_r3v_ch4lleng3_heh3}

Solved by: amkim13