# Pwn - nc
Solved by **ss51**

## Question
Pwn challenges often require connecting to the challenge server using the nc (netcat) command. It's important to learn how to use nc.\

You can connect to the challenge server by executing the following command in your shell. Solve the problem at the connection point and obtain the flag.
## Solution
When you `nc` to the server, it will ask for an answer. download the `main.c` file and from the source code, you'll see:
```
if(answer == 10){
        win();
    }
```
`nc` to the server again, give the answer 10 

### Flag
`FLAG{th3_b3ginning_0f_th3_r0ad_to_th3_pwn_p1ay3r}`
