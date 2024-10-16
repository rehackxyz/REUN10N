# The Investigator

Solved by: @kreee00

## Question:
Help Jieyab found the newspaper. When was this newspaper published?

The flag name is date TCP1P{Date Month Year}

## Solution:

### Challenge Overview:

In this challenge, I was given an image of a newspaper with the headline "PETRUS roeit Indonesische misdaad uit". The objective was to identify the original article and extract relevant information.

### Step 1: Initial Search Attempts

Following my success in a previous challenge, I decided to try reverse image searches on both Yandex Image Search and Google Image Search. Unfortunately, neither provided any relevant matches or similar images. I realized I would need to approach this problem differently.

### Step 2: Recognizing the Language

I observed that the newspaper was in Dutch, so I decided to search for Dutch newspaper archives online. A simple Google search for "Dutch newspaper archive" led me to two valuable resources:

- [Radboud University Library's News Archive](https://libguides.ru.nl/news/delpher)
- [Delpher Digital Dutch Archives](https://www.delpher.nl/)

### Step 3: Accessing the Archive

While the first link provided general information about accessing Dutch newspapers, the second link led me to Delpher, a comprehensive Dutch newspaper archive. However, Delpher's website required a VPN to access in my region (Malaysia).

After activating the VPN, I proceeded to search for the main headline visible in the image: "Links Frankrijk wil rechtse pers breken". This was a crucial move, as it led me directly to the full, uncropped version of the article in question.

### Step 4: Verifying the Date

Upon viewing the full article, I quickly found the key piece of information: the newspaper's publication date was clearly visible at the top left corner of the page, confirming the timeline of the event.

**Flag:** `TCP1P{17 December 1983}`
