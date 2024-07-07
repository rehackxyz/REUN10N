# emuc2
Solved by **warlocksmurf**\
Full writeup is available at https://warlocksmurf.github.io/posts/ductf2024/#emuc2-forensics

## Question
As all good nation states, we have our own malware and C2 for offensive operations. But someone has got the source code and is using it against us! Here’s a capture of traffic we found on one of our laptops…

## Solution
decrypt tls > obtain credentials for a login page > cant login cuz invalid JWT > get the real JWT from one of its upload files in `/api/env` > encode the real JWT and use it when logging in

![1](https://i.ibb.co/NpKJTLM/Screenshot-2024-07-07-232625.png)

Looking into HTTP2? Why HTTP2 because it was encrypted before.
![2](https://i.ibb.co/h1NYrpt/Screenshot-2024-07-07-232756.png)

![3](https://i.ibb.co/NskNJvv/Screenshot-2024-07-07-233316.png)

Since cannot access due to JWT token wrong, need to find any file that contains JWT secret so that our modification JWT are acceptable. 
```
import jwt

data = {"subject_id": 1, "exp": 1920187883}
JWT_SECRET = "3gHsCBkpZLi99zyiPqfY/NfFJqZzmNL4BAhYN8rAjRn49baTcnmyGISLD6T58XcWIUYrBfltI2iq2N6OHQSrfqBRFxFta61PvmnfRyn8Ep8T55lvLT8Es62kN3x35Bcb0OZmOGmM/zKf2qadcBq3Nbq1MiIVKJMz4w3JOk4orwFPtSNpNh8uaSQQUNMKTT6cvD9bvRvFNeeHYSPhDFwayPIRr5TJ+BpIRTUTfc1C3WCKoOuXCz2t+ISZo5yYwZ6U5w7NKFTTuDqMP/dXevkVykuntdej55XE3fsCP+UVFUT2JrY+Z9Q1aKTgavQR5smYVn93RlpbFwCoSStoANnoi"

encoded = jwt.encode(data, JWT_SECRET, algorithm="HS512")
print(encoded)
```

### Flag
`DUCTF{pǝʇɔǝɟuᴉ_sᴉ_ǝlᴉɟ_dᴉz_ǝɥʇ_oʇ_pɹoʍssɐd_ǝɥʇ}`
