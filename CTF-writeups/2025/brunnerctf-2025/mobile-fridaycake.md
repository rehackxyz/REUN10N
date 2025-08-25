We get a apk file call FridayCake.apk. After execute in emulator, we can see that we need to key in some secret code to get the flag(maybe) and given (Recover the Secret Access Code and save the family's cake tradition.). I use jadx to decompile it and we can see the package call dk.brunnerctf.fridaycake after read through there is a class call NativeChecker

public final native String getDecryptedFlag();
public final native boolean verifyCode(String code);
this two interesting methods show up.

so i suggest using Frida to hook it and call the methods directly at runtime will solve.
my script

```
Java.perform(() => {
  const inst = Java.use('dk.brunnerctf.fridaycake.NativeChecker').INSTANCE.value;
  inst.verifyCode("testtest"); // actually anything will do
  console.log(inst.getDecryptedFlag());
});
```

Flag: brunner{Y0u_Us3d_Fr1d4_F0r_Gr4bb1ng_Th1s_R1ght?}

Solved by: w_11_xuan