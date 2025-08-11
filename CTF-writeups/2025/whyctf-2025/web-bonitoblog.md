## Description
We created a [blog](https://bonitoblog.ctf.zone), now go write your life story like everyone else!

## Solution
There is an IDOR vulnerability in /blog/update that allows you to assign an editor to other people's posts. This is a bit guessy, but the flag that we want is at /blog/1337 

Without permissions, we get "You are not allowed to view this content". To exploit, you need to create your own account, create a new blog post, and intercept the request when you add a new editor. Update the `postId` parameter to 1337 and you'll get a 302 :)

`postId` in URL must be a blog post that you have permissions to.


Flag: flag{5a593f66535c10f2291a8dcb8e88bfbb}

Solved by: benkyou