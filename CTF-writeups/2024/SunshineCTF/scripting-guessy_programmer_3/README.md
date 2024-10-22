# Guessy Programmer 3

Solved by: @n3r, @OS1R1S

## Question:
Adventurer beware!

This challenge is not for the faint of heart.

ł ₴ɆɆ ₮₩Ø ₮Ɏ₱Ɇ₴ Ø₣ ₱ɆØ₱ⱠɆ: ₮ⱧØ₴Ɇ ₩ⱧØ ₳ⱤɆ ₩łⱠⱠł₦₲ ₮Ø ₴Ɇ₳Ɽ₵Ⱨ ฿ł₦₳ⱤłɆ₴... ₳₦Đ ₮ⱧØ₴Ɇ ₩ⱧØ ₳ⱤɆ ₦Ø₮.

G̴̵͈̥̣͉ͩ̌̓̽ͦ̕͡o̷̢̗̗͙̦̼̞̳̝͖̼̘͙͎̝̹̍ͭ̂͊͒͗̀͊͛̐̈̊͋͒̅̓͊̍̌ͣͥ͛̕͟͝͠o̷̵͖͍͓͙͇̣͇̻̟̜ͬͮ͋ͧͦͦ̋͋̒̀̏͆̈̿ͭ̈́͑̚͡d̵ͥͩ ĺ̟̖͎͔̜̙͚͉͍̰̤ͥ̊͒ͧ̊ͩ͂͌̾͒͌̽̓̐ͪ̆̔̊̎̓ͤ͊ͩ̔͘͞ͅu̶̜̘̠̐͑ͩ̄͌ͩ͌̉͋͜͞c̴̴̶̴͔̲͚̬̦̳͇͈̹̀̇̇̀̈́̄̾̍̉̔́̒̌͆̐̽̍ͣ͟k̯̻̉̓ͪ̀͜ t̴̬͍̯̹̪̳ͫ͐͛ͩ̉ͥ͒̉͗̚͘͟_̆̈́ͫŕ̸̸̷̲͍̞̹̠̰̰͈̭̦̹͍͇̒̃͊̈́̾̏̈́ͮ̒̑͗ͤ̆̄͂̀̆͌͑̾́̚͟͢͜͟͡͡͝ȧv̸͓ͬ͒ͤ̕͜͜_̼̮͍̟̘̝ͫͩ̔̀̅̊̓ͪ̎̏̀e̵̟̥͍͎͈̠̊ͭ͑̒̐̑͒̔͂ͪͪ͞l̵̪̞̥̘̩͓̻͙̺̮ͮ͒ͤͣ͗ͩ̉ͣͩ͐̏̽ͭ͆ͫ͢͢͞ȩ͇̤̭̖̈̿͋̓ͮͥŗ̛̠̲̣̭̝̯̜̙͎̻̲̯̒̿͑̋͋ͣ̾́̈̉̓͆͢͜.̷̨̢͇̟͔̫͈͇͙̐͆̿ͬ̄̃ͭͦ̀̅̑̃̃̍̈̐͟͞ͅͅͅͅ

𝐌⃥⃒̸𝐚⃥⃒̸𝐲⃥⃒̸ 𝐰⃥⃒̸𝐞⃥⃒̸ 𝐦⃥⃒̸𝐞⃥⃒̸𝐞⃥⃒̸𝐭⃥⃒̸ 𝐚⃥⃒̸𝐠⃥⃒̸𝐚⃥⃒̸𝐢⃥⃒̸𝐧⃥⃒̸,⃥⃒̸ 𝐨⃥⃒̸𝐧⃥⃒̸ 𝐦⃥⃒̸𝐨⃥⃒̸𝐫⃥⃒̸𝐞⃥⃒̸ 𝐝⃥⃒̸𝐞⃥⃒̸𝐜⃥⃒̸𝐞⃥⃒̸𝐧⃥⃒̸𝐭⃥⃒̸ 𝐭⃥⃒̸𝐞⃥⃒̸𝐫⃥⃒̸𝐦⃥⃒̸𝐬⃥⃒̸.⃥⃒̸

PS
Only persons ignorant of regexes (regexi?) deal in absolutes.

Which come to think of it is an absolute statement.

Well... you can kill my regexes (regexi?), but you will never destroy them! They will always be legacy code!

(([Oo][Bb][Ii])-+([Ww][Aa][Nn]) ?(K[Ee][Nn][Oo][Bb][iI])+)????

## Solution:
```
#!/bin/bash

if [ ! -d .git ]; then
    echo "This script must be run in a Git repository."
    exit 1
fi

commit_hashes=$(git log --pretty=format:'%H')

for commit_hash in $commit_hashes; do
    echo "Checking out commit: $commit_hash"
    
    git checkout "$commit_hash" -- adventure_novel_3.gif
    
    if [[ -f adventure_novel_3.gif && -s adventure_novel_3.gif ]]; then
        file_content=$(cat adventure_novel_3.gif)

        base64_strings=$(echo "$file_content" | grep -oP '[A-Za-z0-9+/=]+' | grep -E '^([A-Za-z0-9+/=]{4})+$')

        for base64_string in $base64_strings; do
            decoded_value=$(echo "$base64_string" | base64 --decode 2>/dev/null)

            if [ $? -ne 0 ]; then
                echo "Error decoding base64 string: $base64_string"
                continue
            fi
            
            if [[ $decoded_value == *"sun{"* && $decoded_value == *"}"* ]]; then
                echo "Found 'sun{' and '}' in the decoded value at commit $commit_hash."
                echo "Decoded value: $decoded_value"
                break 2 
            fi
        done
    else
        echo "The file adventure_novel_3.gif is either missing or empty in commit $commit_hash."
    fi
done
git checkout -

```

**Flag:** `sun{u_realize_you_could_have_converted_the_gitattributes_to_be_text_with_a_refactor_and_then_just_solve_it_as_normal_oh_well_strings_also_works}`
