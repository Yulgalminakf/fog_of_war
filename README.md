# fog_of_war
A fog of war calculator.
Early alpha. There will be bugs, slowdowns, and it's a bit specific and arbitrary in its use. Deal with it.

Requires a few things to work:

1.  This is written in python. I used Anaconda3: https://www.continuum.io/downloads
    Install it.
    
2.  I'm using my own module full of random utility code. I call it juc (Just Utility Code).
    You can find it on this site under my name as well.
    
3.  This is also using pillow. Open up a command prompt and type:
          pip install Pillow
    or, if you know what you're doing, just install pillow however you want.

Usage:

This takes a black and white .png image and runs a fog of war calculator on it.
This site http://donjon.bin.sh/5e/dungeon/ has a good dungeon generator. 
  Grid must be None
  Map Style must be Standard
  Dungeon Layout can be anything you want, but Cavernous works best. So far, this doesn't work with doors, nor anything else that can be generated with it.
Once you have it downloaded, open it up in paint/gimp/photoshop/etc, and remove the numbers/letters. Keep a copy of the original if you want to be able to reference them later.
So far, it only works with black and white images, and doors must be removed.
