# The Pentagon

Solved by: @kreee00

## Question:

A few days ago, I saw a funny post on a social media platform.
As far as I remember, there are five accounts that frequently post funny and random content.
I only remember two names: Udin Kurniawan Jaeger and Paijo Abdul Uchiha.
I recall that one of them uses a fake account. The humor in his posts is quite random, and I like it.
I want to know the real name of the person using that second account because I want to connect with him on his main account.
Please help me find his full real name.
The flag is the full name

Example: TCP1P{Kresna Yang Asli}


## Solution:

### Challenge Overview:

In this challenge, we were provided with two suspicious names: *Udin Kurniawan Jaeger* and *Paijo Abdul Uchiha*. The task was to track their online presence and follow clues to obtain the flag.

### Step 1: Google Search for Usernames

I began by performing a quick Google search on both names. This led me to discover that they were previously associated with Reddit accounts. Unfortunately, both accounts had been either suspended or deleted, so this avenue didn’t provide any further leads.

### Step 2: Using Sherlock to Investigate Usernames

Next, I decided to use [Sherlock](https://github.com/sherlock-project/sherlock), a tool for finding usernames across social media platforms. I ran the following command:

```
sherlock ud1nwanj4eger paij0uch1h4
```

This revealed that both users had active accounts on 9gag. I started browsing *ud1nwanj4eger*'s 9gag posts and eventually came across a particular post that had 14 comments.

![image](https://github.com/user-attachments/assets/23948ecd-9aa7-443f-9e32-eb28ff6f94a4)


### Step 3: Digging Through the Comments

I examined each of the comments carefully and found a potential clue in one of them.

![image](https://github.com/user-attachments/assets/a759126f-e130-4420-9013-5e11d1d97313)


At first glance, I assumed it was another 9gag link, so I attempted to visit the URL: `https://9gag.com/u/DAJjWLRzVpw`. However, nothing came up on the 9gag site.

### Step 4: Recognizing the Instagram Hint

Upon re-reading the comment, I realized it mentioned "that app with the photo logo," which made me think of Instagram. So, I changed the link format to:  
`https://www.instagram.com/p/DAJjWLRzVpw/`. 

This led me to an Instagram post, and in the bio of the account, I found the phrase "Second Account," which was referenced in the challenge.

### Step 5: Discord Link and Interaction with Bot

The Instagram bio contained a link that directed me to a Discord channel. Once in the channel, I encountered a bot with the same username as the one in the challenge. I tried sending it a message, but it replied with:

![image](https://github.com/user-attachments/assets/16b3e1a8-dc55-47c0-a479-8c75a60c32e1)


### Step 6: Analyzing Instagram Posts for Hidden Clues

Afterward, I watched each of the Instagram account's posts. One video had distorted audio, so I downloaded the audio and opened it in Audacity for further analysis. Playing the audio at half speed didn’t provide any clear information, so I decided to reverse the track.

**Voila!** The reversed audio revealed a password:  
`tcp1p_th3p3nt490n_1s4w3s0m3`

I sent this password to the bot in the Discord chat, and finally:

![image](https://github.com/user-attachments/assets/a78c668f-b324-4344-be83-2ee8fe35d97b)


The bot responded with a link, which led me to the flag.

**Key Learnings:**

- Sherlock is a powerful tool for identifying usernames across various platforms.
- It's important to consider alternate interpretations of URLs (in this case, switching from 9gag to Instagram).
- Tools like Audacity can help uncover hidden clues embedded in audio files.
  

**Flag:** `TCP1P{Slamet Setiawan Uzumaki}`
