# Number Mashing
Solved by **whymir**

## Question
Mash your keyboard numpad in a specific order and a flag might just pop out!

## Solution
Run the file at first to see what programs it is. Then open the ghidra to do more analysis on it

![a](img.png)

There is logic where it can be concluded as, `Val 1` and `Val 2 != 0` and `Val 2 != 1`. `HoldingValue == Val 1 / Val 2`. Vulnerability occurs here where it does not check input which mean can be negative. `Val 2 = -1`. For `Val 1` always return `Val 1` after divided is when it reaches the maximum number in the `int` range which was `-2,147,483,647` to `2,147,483,647`. If we put `2,147,483,648` it will always return `2,147,483,648`. Why? It wraps the overflow value. 

![b](img.png)

### Flag
`DUCTF{w0w_y0u_just_br0ke_math!!}`
