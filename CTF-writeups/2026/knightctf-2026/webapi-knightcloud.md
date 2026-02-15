# web/api - KnightCloud

The Vulnerability: Internal Migration Helper
Looking at the bottom of the script, there is an object exposed to the global window scope called KC_INTERNAL. It contains a helper function updateUserTier that sends a request to an internal API endpoint.

```
// Found in your source code:
helpers: T,
examples: {
    upgradeUserExample: {
        endpoint: "/api/internal/v1/migrate/user-tier",
        method: "POST",
        body: {
            u: "user-uid-here",
            t: "premium"
        },
        validTiers: ["free", "premium", "enterprise"]
    }
}
```

click Load Analytics button under 📈 Advanced Analytics
Flag: `KCTF{Pr1v1l3g3_3sc4l4t10n_1s_fun} `

Solved by: Ha1qal

Solved by: yappare