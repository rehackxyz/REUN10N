# Corporate Life 1
Solved by: @aan
### Question
The Request Management App is used to view all pending requests for each user. It’s a pretty basic website, though I heard they were working on something new.

Anyway, did you know that one of the disgruntled employees shared some company secrets on the Requests Management App, but it's status was set _denied_ before I could see it. Please find out what it was and spill the tea!

### Solution:
1. Analyze `/_next/static/bkat3_n9dfvE_URrWvN1g/_buildManifest.js`
2. Noticed interesting endpoint `sortedPages:["/","/_app","/_error","/v2-testing"]}` 
3. Visit `/v2-testing`, when filtering data, it will request data from new API endpoint at `/api/list-v2` 
4. that endpoint is vulnerable to NoSQL injection with this payload, can list all employees
`{"filter":"' or 1=1-- -"}`

**Flag:** `KashiCTF{s4m3_old_c0rp0_l1f3_zTQ6KRfZ}`

