# Solution

File upload vulnerability + race condition allow you to upload a webshell to the application and read the flag.

Make a solver script that interacts with the chall to understand the behaviour(file names after being uploaded).

Then multithread uploading it and accessing it so that you have a chance to actually access the shell n run the command to get the flag

