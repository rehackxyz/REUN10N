# Solution
```
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;

    int dp[3] = {-1000000000, -1000000000, -1000000000}; // use int literal

    for (int cat : a) {
        // Copy current value to compare later
        int val0 = dp[0], val1 = dp[1], val2 = dp[2];

        // Start new sequence at current category
        dp[cat] = max(dp[cat], 0);

        if (cat == 0) {
            dp[0] = max({dp[0], val1 + 4, val2 + 1});
        } else if (cat == 1) {
            dp[1] = max({dp[1], val0 + 2, val2 + 6});
        } else if (cat == 2) {
            dp[2] = max({dp[2], val0 + 3, val1 + 5});
        }
    }

    cout << *max_element(dp, dp + 3) << '\n';
    cout.flush();
}
```

flag: `grey{1m_s0m3whaT_oF_4_c0mp3tit1vE_pR0gramm3R_mYsELF}`

Solved by: yappare