# notcrypto

Solved by: @0x251e

## Question:
You shouldn't need to call your crypto teammate for this challenge lol.


## Solution:
```go
package main

import (
	"fmt"
)

func main() {
	encryptedData := []byte{
		22, 45, 121, 202, 86, 198, 101, 233, 233, 22, 102, 35, 9, 45, 27, 9,
		28, 9, 198, 28, 31, 173, 233, 218, 160, 198, 26, 102, 9, 173, 129, 28,
		128, 57, 160, 33, 9, 101, 45, 48, 246, 87, 246, 162, 101, 101, 33, 162,
		120, 120, 120, 120, 120, 120, 120, 120,
	}

	data4050 := []byte{
		99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
		202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
		183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
		4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
		9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
		83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
		208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
		81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
		205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
		96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
		224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
		231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
		186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
		112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
		225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
		140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22,
	}

	inverseData4050 := make([]byte, 256)
	for i, val := range data4050 {
		inverseData4050[val] = byte(i)
	}
	reverseTransformation := func(chunk []byte) []byte {
		currentState := make([]byte, 8)
		copy(currentState, chunk)
		for i := 4095; i >= 0; i-- {
			r14 := currentState[0]
			r10 := currentState[1]
			r8 := currentState[2]
			rbx := currentState[3]
			rdi := currentState[4]
			r9 := currentState[5]
			r15 := currentState[6]
			rbp := currentState[7]
			oldR15 := inverseData4050[byte((int(r14)^i)%256)]
			oldR14 := inverseData4050[byte((int(r10)^i)%256)]
			oldRbp := inverseData4050[byte((int(r8)^i)%256)]
			oldRbx := inverseData4050[byte((int(rbx)^i)%256)]
			oldRdi := inverseData4050[byte((int(rbp)^i)%256)]
			oldR10 := inverseData4050[byte((int(rdi)^i)%256)]
			oldR8 := inverseData4050[byte((int(r15)^i)%256)]
			oldR9 := inverseData4050[byte((int(r9)^i)%256)]
			currentState = []byte{
				oldR14,
				oldR10,
				oldR8,
				oldRbx,
				oldRdi,
				oldR9,
				oldR15,
				oldRbp,
			}
		}
		return currentState
	}
	var chunks [][]byte
	for i := 0; i < len(encryptedData); i += 8 {
		end := i + 8
		if end > len(encryptedData) {
			end = len(encryptedData)
		}
		chunks = append(chunks, encryptedData[i:end])
	}
	var flag []byte
	for _, chunk := range chunks {
		reversedChunk := reverseTransformation(chunk)
		flag = append(flag, reversedChunk...)
	}
	flagStr := string(flag)
	fmt.Println("Flag:", flagStr)
}
```


**Flag:** `x3c{pwndbg_and_pwntools_my_belowed_573498532832}`
