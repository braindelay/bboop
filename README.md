# BibblyBoop 

## What is this?

The work of an eleven year old learning python after coming from `scratch`.

- The triangle of **BOOPS** are coming down from the top.
- Fire your **BIBBLE** at them, it will stick to them
- If your **BIBBLE** touches two or more **BOOPS** of the same colour they will drop off the screen.
- If, after this, there are any **BOOPS** that have been left unattached from the top row, they will drop off the screen, too.
- You lose if the **BOOPS** make it to the bottom of the screen
- You win once all the **BOOPS** jave have been knocked-off.

## Why did we do this in python? 

- It was harder to do the sprites in python, but `pygame` did a lot of the work.
- Finding out which balls were touching which other balls - and then what other balls _they_ were touching (and so on) would have been a _nightmare_ in scratch.
- There are cleaner ways to write this, but they need some maths an elevlen year old wouldn't get - so we did it the simple way (although it's a little slow)

## Development

A `python3` game, the requirements are in the `requirements.txt` fileudo apt install python3-pip

To install and run on linux, run this from inside the directory of the project.

```bash
# create a virtual env
python3 -m venv venv

# install stuff
source ./venv/bin/activate

python3 -m pip install -r requirements.txt

# do stuff
python3 bboop.py
```
And on windows:

First install python3: https://www.python.org/downloads/windows/

Then inside the directory of the project

```bash
# create a virtual env
python3 -m venv venv

# install stuff
venv\Scripts\activate

python3 -m pip install -r requirements.txt

# do stuff
python3 bboop.py
```





    


## Anything else?

- Maybe add sound, a beep every time the boops slide?
- Maybe have the speed that the boops slide get faster over time and have the beeps get faster, to scare the player ;) 
- Maybe change the logic that picks the bibble's colour to only uses colours being used by the available boops? Check out `sets` for this

The next two need to wait until you know some harder maths
- The hitchecker could be done better using graph theory, check out `scipy` (wouldn't hold this against the 11 year old that wrote it ;) ) 
- The code for moving loops 10 times in steps of 1 - when you learn vectors there are easier ways to do this without having the same collision bugs
