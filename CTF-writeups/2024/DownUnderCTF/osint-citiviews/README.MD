# cityviews
Solved by **yappare**

## Question
After having to go on the run, I've had to bunker down. Which building did I capture this picture from?

NOTE: Flag is case-insensitive and requires placing inside DUCTF{}! e.g DUCTF{building_name}

## Solution
![cityview](https://i.ibb.co/q0JVV3v/cityviews.jpg)
From the provided image, we used Geospy.Ai to give us some ideas. The result stated it was somewhere in Melbourne. We narrow down by observing two things:
- the shape of the windows
- the building behind it that looks like a clock tower

After several checks, we confirmed the location:
https://www.google.com/maps/@-37.8200792,144.9551686,122a,35y,231.69h/data=!3m1!1e3?entry=ttu

### Flag
`DUCTF{hotel_indigo_melbourne}`
