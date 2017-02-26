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

Hotkeys:
    R: Opens a dialogue to input radius. Radius is considered in pixel size. 100 by default.
    L: Toggles between whether or not it considers LoS(Line of Sight). On by default.
Note: None of the options are saved to disk. They are per run of the script and will go back to the default when you close and reopen it.

This takes a black and white .png image and runs a fog of war calculator on it.
This site http://donjon.bin.sh/5e/dungeon/ has a good dungeon generator. 
  Grid must be None
  Map Style must be Standard
  Dungeon Layout can be anything you want, but Cavernous works best. So far, this doesn't work with doors, nor anything else that can be generated with it.
Once you have it downloaded, open it up in paint/gimp/photoshop/etc, and remove the numbers/letters. Keep a copy of the original if you want to be able to reference them later.
So far, it works with black and white floor plans ONLY. Stairs, doors, and other symbols do not work yet.

When you run it, it will prompt you to open up a png. Even if you've run this before, choose the full map version of the png.
If it's your first time running it, it will simply display the entire png. Click on the image wherever you want it to have the starting point.
This script will create two files: name_of_png_states and name_of_png_WorkingCopy.png
The ...WorkingCopy.png will be the currently displayed area saved to the disk (for future use if wanted).
Once you have selected a starting point, it will run the FoW calculator (this takes several seconds, longer if your radius is too high).
You can know the FoW calc is running by either looking at the name of the window, or by monitering the console that popped up.
Once the FoW is done calculating, it'll display the new portion of the map that's visible.
You can click again and again and again (but only in the white-space) to run the FoW calculator centered on the new point.
