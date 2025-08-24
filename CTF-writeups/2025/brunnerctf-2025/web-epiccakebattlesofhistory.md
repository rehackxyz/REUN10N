Referring to package.json it shows that next.js is running on version 15.2.2 which vulnerable to this CVE https://projectdiscovery.io/blog/nextjs-middleware-authorization-bypass

To access the /admin (which is protected by middleware) you can refer to the PoC which is to use the `X-Middleware-Subrequest` header together with this payload `src/middleware:src/middleware:src/middleware:src/middleware:src/middleware`

flag `brunner{0th3llo-iz-b3st-cake}`

Solved by: aan03