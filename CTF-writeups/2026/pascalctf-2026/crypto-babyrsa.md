# crypto - baby-rsa

SOLVED by Jigenz

Try to observe that the binary accepts a single line of input and uses ⁨serde_json⁩ to deserialize it into a rust structure.

Rev the ⁨Deserializer⁩ implementations to find the required field names and types:

```
Root: pascal (String), CTF (u64), crab (Object)
Crab: I_ (bool), crabby (Object), cr4bs (u64)
Crabby: l0v3_ (Array of Strings), r3vv1ng_ (u64)
```

