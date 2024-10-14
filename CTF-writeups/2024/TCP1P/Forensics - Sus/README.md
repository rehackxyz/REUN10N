# Sus

Solved by: @arifpeycal (First Blood!)

## Question:
I received this file from my boss's email, but when I opened it, suddenly all my files got encrypted and I got blackmailed :(((. At least please help me recover my files

## Solution:
1. use `john` to crack zip file (password is `infected`)
2. use `oletools` on `docm` file. (the macro will download a file from https://gist.githubusercontent.com/daffainfo/20a7b18ee31bd6a22acd1a90c1c7acb9/raw/670f8d57403a02169d5e63e2f705bd4652781953/test.ps1)
3. go to the link, deobfuscated powershell script (it will encrypt file using AES)
4. use chatgpt to create decrypt script
5. decrypt `flag.zip.enc` and `password.txt.enc`
6. use password in txt file to open `flag.zip`

```
function Decrypt-AES {
    param (
        [byte[]]$encryptedContent,  # Encrypted content from the file
        [byte[]]$key,               # AES key (must match encryption key)
        [byte[]]$iv                 # Initialization Vector (must match encryption IV)
    )

    # Create AES instance
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $aes.Key = $key
    $aes.IV = $iv

    # Create AES Decryptor
    $decryptor = $aes.CreateDecryptor()

    # Decrypt the encrypted content
    $decryptedData = $decryptor.TransformFinalBlock($encryptedContent, 0, $encryptedContent.Length)

    # Clean up
    $aes.Dispose()

    return $decryptedData
}
function Decrypt-FolderFiles {
    param (
        [string]$folderPath,  # Path to the folder containing encrypted files
        [byte[]]$key,         # AES key (must match encryption key)
        [byte[]]$iv           # Initialization Vector (must match encryption IV)
    )

    # Get all encrypted files with the '.enc' extension
    $encryptedFiles = Get-ChildItem -Path $folderPath -Filter "*.enc"

    foreach ($file in $encryptedFiles) {
        # Read encrypted file content as byte array
        $encryptedContent = [System.IO.File]::ReadAllBytes($file.FullName)

        # Decrypt the file content using AES
        $decryptedData = Decrypt-AES -encryptedContent $encryptedContent -key $key -IV $iv

        # Create new filename by removing the '.enc' extension
        $decryptedFileName = $file.FullName -replace '\.enc$', ''

        # Write the decrypted data to the new file
        [System.IO.File]::WriteAllBytes($decryptedFileName, $decryptedData)

        # Optionally, remove the encrypted file after decryption
        Remove-Item $file.FullName
    }
}
# Decode the key and IV from Base64 string (same as used in encryption)
$base64KeyIV = "K34VFiiu0qar9xWICc9PPHYue/KNLMVO2/HRpVrifikAAQIDBAUGBwgJCgsMDQ4P"
$keyIVBytes = [System.Convert]::FromBase64String($base64KeyIV)

# Extract key and IV from the decoded byte array
$key = $keyIVBytes[0..31]  # First 32 bytes for the key
$iv = $keyIVBytes[32..47]  # Next 16 bytes for the IV

# Define the folder path where encrypted files are stored
$folderPath = "$env:USERPROFILE\Documents"

# Decrypt all '.enc' files in the specified folder
Decrypt-FolderFiles -FolderPath $folderPath -key $key -IV $iv

```

**Flag:** `TCP1P{thank_g0ddd_youre_able_to_decrypt_my_files}`
