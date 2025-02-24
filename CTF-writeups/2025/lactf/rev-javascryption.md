# Javascryption

Solved by: @yappare
### Question: 
You wake up alone in a dark cabin, held captive by a bushy-haired man demanding you submit a "flag" to leave. Can you escape?
### Solution:
1. The hardcoded base64 string was decoded.
2. URL encoding was reversed
3. \[OLD_DATA] was replaced with Z
4. The string was reversed.
5. The resulting Base64 string was decoded to reveal the flag

cabin.js:
```js
const msg = document.getElementById("msg");
const flagInp = document.getElementById("flag");
const checkBtn = document.getElementById("check");

function checkFlag(flag) {
    const step1 = btoa(flag);
    const step2 = step1.split("").reverse().join("");
    const step3 = step2.replaceAll("Z", "[OLD_DATA]");
    const step4 = encodeURIComponent(step3);
    const step5 = btoa(step4);
    return step5 === "JTNEJTNEUWZsSlglNUJPTERfREFUQSU1RG85MWNzeFdZMzlWZXNwbmVwSjMlNUJPTERfREFUQSU1RGY5bWI3JTVCT0xEX0RBVEElNURHZGpGR2I=";
}

checkBtn.addEventListener("click", () => {
    const flag = flagInp.value.toLowerCase();
    if (checkFlag(flag)) {
        flagInp.remove();
        checkBtn.remove();
        msg.innerText = flag;
        msg.classList.add("correct");
    } else {
        checkBtn.classList.remove("shake");
        checkBtn.offsetHeight;
        checkBtn.classList.add("shake");
    }
});
```

**Flag:** `lactf{no_grizzly_walls_here}`
