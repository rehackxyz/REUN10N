1. During execution, the malware initializes the COM library on its main thread. Based on the imported functions, which DLL is responsible for providing this functionality? (filename.ext)
Ans: `ole32.dll`

2. Which GUID is used by the binary to instantiate the object containing the data and code for execution? (********-****-****-****-************)
Ans: `dabcd999-1234-4567-89ab-1234567890ff`

3. Which .NET framework feature is the attacker using to bridge calls between a managed .NET class and an unmanaged native binary? (string)
Ans: `COM Interop`

4. Which Opcode in the disassembly is responsible for calling the first function from the managed code? (** ** **)
Ans: `FF 50 68`

5. Identify the multiplication and addition constants used by the binary's key generation algorithm for decryption. (*, **h)
Ans: `7, 42h`

6. Which Opcode in the disassembly is responsible for calling the decryption logic from the managed code? (** ** **)
Ans: `FF 50 58`

7. Which Win32 API is being utilized by the binary to resolve the killswitch domain name? (string)
Ans: `getaddrinfo`

8, Which network-related API does the binary use to gather details about each shared resource on a server? (string)
Ans: `NetShareEnum`

9. Which Opcode is responsible for running the encrypted payload? (** ** **)
Ans: `FF 50 60`

10. Find → Block → Flag: Identify the killswitch domain, spawn the Docker to block it, and claim the flag. (HTB{*******_**********_********_*****})
Ans: `HTB{Eternal_Companions_Reunited_Again}` //killswitch domain = k1v7-echosim.net 


Solved by: 1337_flagzz