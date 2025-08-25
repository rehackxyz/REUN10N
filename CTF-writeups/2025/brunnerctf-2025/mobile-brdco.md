This is a Flutter challenge. The goal is to enter a valid coupon to retrieve the flag. All the flag checking logic happens client-side, no network requests are made here.

The app does the coupon validation through native C calls using `dart:ffi`. So our app looks something like:
```
Java loadLibrary(flutter) <-> DartVM (daart:ffi to libnative.so) <-> libnative.so
```
You can see this after decompiling the flutter native libraries with blutter. You can use my docker image [here](<https://github.com/benkyousec/blutter-docker>).

In `asm/masterbaker/models/nativeinterface.dart` line 303.
```
    // 0x31cc24: r16 = "libnative.so"
    //     0x31cc24: add             x16, PP, #0xd, lsl #12  ; [pp+0xd650] "libnative.so"
    //     0x31cc28: ldr             x16, [x16, #0x650]
    // 0x31cc2c: str             x16, [SP]
    // 0x31cc30: r0 = _open()
    //     0x31cc30: bl              #0x31cf50  ; [dart:ffi] ::_open
```

The native call in `asm/masterbaker/models/coupon_validator.dart` line 313
```
    // 0x31ecfc: r0 = _callNativeValidation()
    //     0x31ecfc: bl              #0x31ed4c  ; [package:masterbaker/models/coupon_validator.dart] CouponValidator::_callNativeValidation
```
Next, you will have to reverse `libnative.so` . `process_data_complete` is called after loading the native interface from `_callNativeValidation`. Basically we can hook the return value of `FUN_001021B4` to bypass the check and afterwards it will print the flag. Note that the native call only happens when you press on the "Check" button.

![alt text](/CTF-writeups/2025/brunnerctf-2025/images/brdco-couponcheck.png)

To hook `libnative.so` called by flutter, I used `dl_open`. Then you can hook the C functions using offsets from ghidra, just make sure to subtract the base image offset.

Frida script:
```javascript
var do_dlopen = null;
var call_constructor = null;

Process.findModuleByName("linker64").enumerateSymbols().forEach(function (symbol) {
    if (symbol.name.indexOf("do_dlopen") >= 0) {
        do_dlopen = symbol.address;
    }
    if (symbol.name.indexOf("call_constructor") >= 0) {
        call_constructor = symbol.address;
    }
});

// process_data_complete 0x00101f6c
// image base at 0x00100000
var IMAGE_BASE = 0x00100000;
var process_data_complete_offset = 0x00101f6c - IMAGE_BASE;
// coupon check 0x00101fac
var couponCheck_offset = 0x001021b4 - IMAGE_BASE;

var libnative_loaded = false;
Interceptor.attach(do_dlopen, function () {
    var library_path = this.context.x0.readCString();
    if (library_path.indexOf("libnative.so") >= 0) {
        Interceptor.attach(call_constructor, function () {
            if (!libnative_loaded) {
                libnative_loaded = true;
                var libnative = Process.findModuleByName("libnative.so");
                console.log("[+] Hooked libnative.so at: " + libnative.base);
                // Hooking shenanigans here
                var couponCheck_address = libnative.base.add(couponCheck_offset);
                couponCheck(couponCheck_address);
            }
            // var process_data_complete_address = libnative.base.add(process_data_complete_offset);
            // process_data_complete(process_data_complete_address);
        })
    }
})


function process_data_complete(address) {
    Interceptor.attach(address, {
        onEnter(args) {
            console.log("[+] Hooked process_data_complete.");
            console.log("[+] args0:" + args[0].readCString());
        },
        onLeave(ret) {
            console.log("[+] retval: " + ret.readCString());
        }
    })
}

function couponCheck(address) {
    Interceptor.attach(address, {
        onEnter(args) {
            console.log("[+] Hooked couponCheck.");
        },
        onLeave(ret) {
            ret.replace(0x1);
            console.log("[+] couponCheck status: " + ret.toInt32());
        }
    })   
}
```

![alt text](/CTF-writeups/2025/brunnerctf-2025/images/brdco-flag.png)

Solved by: benkyou