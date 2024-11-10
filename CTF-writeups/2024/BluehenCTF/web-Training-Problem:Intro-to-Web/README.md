# Training Problem: Intro to Web

Solved by: @vicevirus

## Question:
It's nice to have some training problems.

## Solution:
dump the git repo
`./gitdumper.sh https://bluehens-webstuff.chals.io/.git/ .``

extract the repo
`sudo ./extractor.sh ../Dumper/ .``

```
if (md5(password) == "1c63129ae9db9c60c3e8aa94d3e00495"){
          //You logged in!
          // password =  1qaz2wsx
          document.getElementById("page").innerHTML = "You ARE logged in... fetching flag";
          form.classList.add('hide');
          $.ajax({
              method:"get",url:"flagme.php",data:{"password":password},success: function(data){
                 $("#page").html(data);
              }
          })
          ```
Visit https://bluehens-webstuff.chals.io/flagme.php?password=1qaz2wsx
**Flag:`udctf{00ph_g1t_b4s3d_l34ks?}`** 
