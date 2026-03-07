# forensic - power leak

Solved by: p5yd4wk

we were provided with a csv file that contains column of position, guess, trace_num, sample, power_mW
`position`: Byte position in the secret (0-5, so 6 bytes total)
`guess`: The guessed byte value (0-9, so digits only)
`trace_num`: Trace number (multiple traces per guess)
`sample`: Sample index within a trace (0-49, 50 samples per trace)
`power_mW`: Power consumption in milliwatts
since we got position 0-5, the secret is only 6 digit.
sooo we use Correlation Power Analysis (CPA) method to get the secret key
http://wiki.newae.com/Correlation_Power_Analysis reference for CPA

In side-channel attacks, when the correct byte value is being processed, it typically consumes more power than incorrect guesses. This is because:

Correct guesses trigger actual computation operations
Incorrect guesses may be rejected early or processed differently
Power consumption correlates with the Hamming weight (number of 1s in binary) of processed values
Step 1: Identify Key Sample Points

Power consumption spikes occur at specific sample points where computation happens. Analysis showed that samples 20-21 exhibit the highest power consumption and variance, indicating these are the computation points.

Step 2: Analyze Power Consumption

For each position, we:
Extract power values at key sample points (20-21) for all guesses
Calculate average power consumption across all traces for each guess
Identify the guess with the highest average power
after analyzing, we got 7,9,2,9,6,3
just sha256sum the 792963 to get the sha256
thenn got the flag
flag: `EHAX{5bec84ad039e23fcd51d331e662e27be15542ca83fd8ef4d6c5e5a8ad614a54d}`

Solved by: yappare