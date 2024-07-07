# Bad Policies
Solved by **zachwong_02**\
**warlocksmurf** also created the full writeup here https://warlocksmurf.github.io/posts/ductf2024/#bad-policies-forensics

## Question
Looks like the attacker managed to access the rebels Domain Controller. Can you figure out how they got access after pulling these artifacts from one of our Outpost machines?

## Solution
Find Groups.xml

Use gpp-decrypt to decrypt the password


### Flag
`DUCTF{D0n7_Us3_P4s5w0rds_1n_Gr0up_P0l1cy}`
