# Upgraded FEFates Randomizer

This is a barbaric but working improvement of thane89's [Fire Emblem Fates Randomizer](https://gbatemp.net/threads/wip-fire-emblem-fates-randomizer.452268/).

## Screenshots

<p align="center">
	<img src="https://i.imgur.com/XCS6NH0.png" />
	<img src="https://i.imgur.com/8oh3vWK.png" />
</p>

## Features

On the one hand, I refined the randomizer's algorithm in order to provide a more enjoyable game experience. The biggest selling point is the possibility to do a pseudo-Pick My Unit run: if you wish, you can limit yourself to the first 16 units recruited with their classes locked to the ones shown in the `ClassSpread.csv` file generated by the script.

On the other hand, I set out to upgrade the whole Fire Emblem experience by rebalancing weapons and adding several quality of life improvements. Those upgrades are completely optional.

### Randomizer Features

- Each character now gets the stats they would have if they had been assigned the randomized class from the start.
    - For instance, if Ryoma is put in Hinata's recruitment spot (so he will be Lvl 9) and assigned the Archer class, then his stats will be his Lvl 1 stats adjusted with 8 levels of (Ryoma's base growths + Archer class growths);
    - Characters with weak growth rates (Gunter, Fuga, Setsuna, Nyx...) can be buffed so that their total growth rates are at least a certain value (default: 270);
        - In counterpart, it is possible to decrease their total base stats to a certain value to keep things balanced (default: 25). 
            - Fuga becomes completely busted if this is not done.
- Similar to the original randomizer, stats will be shuffled a bit. The default settings are:
    - 10 passes per character, with each pass having:
        - 100% chance of shuffling 5% of growths
        - 50% chance of shuffling 1 stat point
        - 25% chance of shuffling 1 modifier point
- Random swaps of stats / growths / mods can occur (always all three, except for Lck):
    - Str / Mag (default: according to class)
    - Skl / Spd (default: 20% chance)
    - Def / Res (default: 20% chance)
    - Lck / ? (default: [Lck Growth]% chance, only if Lck stat / growth / mod is superior)
- Fixed skill randomization and removed unbalanced ones (Aptitude (108), Bold Stance (120), Point Blank (121), Winged Shield (122), Paragon (138), Armor Shield (139), Beast Shield (140), Taker Skills (142->148), Ballistician skills (149->152), Warp (154))
- "Catch 'em all" mode: minimize duplicate final classes according to the chosen route.

### Upgraded Fates Features
- Dawn / Dusk Armories and Rod / Staff shops available in every route
- Changes to weapon triangles: Tome <-> Axe, Dagger <-> Sword, and Bow <-> Lance become neutral
    - Rationale: range weapons can already hit melee weapons without retaliation so they shouldn't have weapon advantage on top of that
- Weapon Ranks changed; in practice, every rank is matched with the one below. E-rank hell only lasts for one hit now!
	- D 21 -> 2
	- C 51 -> 22
	- B 96 -> 52
	- A 161 -> 97
	- S 251 -> 162
- Weapon Updates: increased the difference between Hoshidan and Nohrian weapons, nerfed the hell out of those busted hidden weapons, doubled Staff Exp for convenience.
	- Swords, Lances, Yumis, Scrolls: +1 Mt, -5 Hit, -5 Avo
	- Katanas, Naginatas, Bows, Tomes: -1 Mt, +10 Hit, +5 Avo
	- Axes: +1 Mt, -5 Hit, -10 Avo
	- Clubs: -1 Mt, +5 Avo, +5 Crit
	- Daggers: -2 Mt, -5 Hit
	- Shurikens: -4 Mt, +5 Avo, -10 Hit, +5 Ddg
	- Staff: Staff Exp x2 for those listed
		- Heal 10 -> 12 Mt
		- Mend 20 -> 25 Mt
		- Physic 7 -> 9 Mt
		- Recover 35 -> 45 Mt
		- Fortify 7 -> 9 Mt
	- Rod: Staff Exp x2 for those listed
		- Bloom Festal 7 -> 4 Mt
		- Sun Festal 14 -> 10 Mt
		- Wane Festal 2 -> 1 Mt
		- Moon Festal 25 -> 20 Mt
		- Great Festal 2 -> 1 Mt

## Instructions

### Requirements

You will need to install [Python](https://www.python.org/), [numpy](https://numpy.org/) and the [xmltodict](https://github.com/martinblech/xmltodict) module. I advise using virtual environments but for the layman a simple
```
pip install numpy xmltodict
```
should do the trick.
The instructions can look daunting but once you understand how it works it takes fewer than 5 minutes to do. Some experience with Python and/or tinkering with files will obviously help though.

0. Begin by either cloning the repository or downloading and extracting the zip.
1. First, choose which version of Fates you want to play:
    - _Vanilla Fates_: for copyright-related reasons, you will have to dump your own romfs. Follow the instructions in thane89's original readme below.
    - _Gay Fates_: _Vanilla Fates_ patched with vastly expanded supports ([original thread here](https://gbatemp.net/threads/fire-emblem-fates-expanded-same-sex-marriage-patch-wip.416109/)). This is very welcome since randomization doesn't touch supports. Extract `fates_gay_decompressed.7z`.
    - _Upgraded Gay Fates_: _Gay Fates_ patched with my curated upgrades listed above. Extract `fates_gay_upgraded_decompressed.7z`.
    - **_Good Guy Garon Upgraded Gay Fates_ (recommended)**: _Upgraded Gay Fates_ with the [Good Guy Garon Edition patch](https://gbatemp.net/threads/release-conquest-story-overhaul-fire-emblem-fates-good-guy-garon-edition.487117/). Extract `fates_gay_upgraded_GGG_decompressed.7z`.
The extracted folder will be referred to as the "romfs" folder.
2. Run `Fates Randomizer Beta 5-5.jar`, click "Open and Verify", and select the romfs folder. You should see a new window pop up with options. If you do not, the window will show you which file was not found.
3. Select a path and options. Options "Anna", "Amiibo Units", and "Children" must be selected. Refer to the original readme below if you do not understand an option. I recommend selecting `All Routes` (even if you plan to play Birthright or Conquest, the Python script has route options too) and all options except the experimental ones and the stat randomization.
4. Hit "Randomize" and let the program sit. When the program finishes, a little notification will pop up in the corner of the window.
5. Close `Fates Randomizer Beta 5-5.jar`.
6. Copy the `RandomizerSettings.xml` file from the romfs folder to the `data` folder.
7. Open a command prompt in the same folder as `updated_randomizer.py`. Run
```
python updated_randomizer.py
```
If you want to know about the options, type
```
python updated_randomizer.py -h
```
8. If the script ran successfully, you should have two files named `RandomizerSettingsUpdated.xml` and `ClassSpread.csv` in the data folder. Otherwise, try to run one more time, and if it fails again, raise an issue on this repository.
    - `ClassSpread.csv` contains on each line the original character, their replacement and the class assigned to the replacement. I recommend respecting the file's assignements for more fun and challenge.
    - `RandomizerSettingsUpdated.xml` contains the detailed information of the randomized run. For each character, the `StringData` and `ClassData` fields are tied to the character while the other fields are tied to their spot. If Ryoma has as "switchingCharacter" Hinata, he will have the stats that are written in Hinata's `Stats` field (but those stats will have been computed as Ryoma's "expected" stats at this spot). I recommend not looking at it for more fun.
10. Delete the romfs folder and repeat steps 1-5 but, in step 3, choose "Custom Path" and select `RandomizerSettingsUpdated.xml`. Don't forget to check the "Join Order" options again if you did previously.
11. Close `Fates Randomizer Beta 5-5.jar`. Open `FEAT.exe`. Drag the romfs folder into FEAT: this will recompress the files. Once FEAT is done, you can close it.
12. Phew! You're done! Now you can copy your roms folder to the mods folder of your gaming medium.
13. As a final note, DO NOT use this on top of an existing save or branch of fate. Use a fresh save starting from the very beginning if you want a stable playthrough.

## Troubleshooting

### Chapter 2: There's an immobile "phantom" unit near the top left corner!
This sometimes happens. Just kill it after the others, you should be able to.

### Chapter 5: This chapter is way too hard!
I advise using the Infinite Movement cheat code for this chapter. If you can play Randomized Fates, you can probably find how to use cheats on your gaming medium.

### Conquest Chapter 9: Talking with Nyx crashes the game!
Break the wall near Nyx before talking to her. 

### Revelations Chapter 8: Hayato was not replaced!
This is an issue from the original randomizer; I can't fix it myself. This can amusingly lead to recruiting two Hayatos.

# Original README by thane98

This is an early version of a class + join order randomizer for Fire Emblem Fates. Keep in mind that the entire tool is a work-in-progress at the moment, so some features may not work as intended. In fact, you could potentially experience crashes depending on which features you are using. A breakdown of features, options, and tool usage can be found below.

## Current Features
- Assign random classes to new characters using proper genders (male character will receive a male class, female characters will receive a female class.)
- Randomize base stats, growths, and stat modifiers without changing totals. If a character starts with 30 points across every stat, they will end with that many. The randomizer only changes where these points are invested.
- Randomize existing skills. At the moment, this feature simply chooses from every available skill in the game. Additional options may be added in the future to allow users to determine which skills the randomizer chooses from.
- Adjust the order that characters join in.
- Adjust cutscenes, sounds, and alternate appearances to match the new join order. For example, if Izana switches with Ryoma, then Izana will appear in Ryoma's place during the prologue, chapter 4, and chapter 6.
- Swap 3D models for cutscenes.
- Randomize children by assigning them to different parents and paralogues.

## Basic Options
Join Order - Switch when characters join you in the story.
Cutscenes - Change cutscene text to reflect the new join order.
Sounds - Change voice lines in cutscenes to match the join order.
Same-Sex - Only swap characters of the same sex.
Models - Change the models used in cutscenes based off of the join order.

Randomize Stats - Enable stat randomization.
Passes - Determines how many times the randomizer will take a point from one stat and add it to another.

Randomize Skills - Enable skill randomization.
Promote Jakob/Felicia - Treat Jakob and Felicia as promoted units when randomizing classes.
DLC Classes - Add DLC classes to the class pool when randomizing.

## Optional Characters
Anna
Amiibo Units (Marth, Ike, Lucina, Robin)
Children

## Experimental Options
Change All Appearances - Change every instance of a character to use their randomized class.

## Instructions
1. Create a folder to use for storing game files. You will need to pick out a specific set of game files from the ROM so that the randomizer can modify them.
2. Create a folder called GameData inside the storage folder. From your ROM, copy GameData.bin.lz and the Dispos and Person folders from the ROM's GameData folder into the one you created.
3. Create a folder called castle inside the storage folder. From your ROM, copy castle_join.bin.lz from the castle folder into the castle folder you created.
4. Copy the m folder and Script folder from your ROM into the storage folder. Your storage folder should look like this:
	Main Directory
		castle
		  castle_join.bin.lz
		GameData
		  dispos
		  person
		  GameData.bin.lz
		m
		Scripts
5. Run FEAT.exe, highlight all of the folders in the storage folder, and drag them into FEAT. The program should decompress every file in the storage folder. Check to make sure that the .bin.lz files now only have a .bin extension.
6. Make a backup of this folder so that you don't have to go through this process again.
7. Run Fates-Randomizer.jar, click "Open and Verify," and select the storage folder. You should see a new window pop up with options. If you do not, the window will show you which file was not found.
8. Select a path and options. Refer to the section above if you do not understand an option. Hit "Randomize" and let the program sit. When the program finishes, a little notification will pop up in the corner of the window.
9. Close Fates-Randomizer.jar and highlight all of the files in the storage folder. Drag them into FEAT like you did previously to recompress them. You can close FEAT it finishes compressing every file.
10. You're done! You can either merge these files in with a ROM if you're using HANS (back up the ROM if you're doing this just in case) or place the files in your patch folder if you're using NTR. Enjoy your randomized adventure!
11. As a final note, DO NOT use this on top of an existing save or branch of fate. Use a fresh save starting from the very beginning if you want a stable playthrough.

## Known Issues

- Lunatic is more unstable than other modes. Crashes have been reported on chapter 2 and chapter 4 when playing on Lunatic.
- Leo's model does not swap correctly during chapter 2's cutscenes, causing a generic model to appear in its place.
- Randomizing without join order turned on will not swap out weapons.
- AI does not behave correctly in certain instances when "Change All Appearances" is turned on.

## Troubleshooting

If you experience any sort of crash, the only way to fix it requires removing the file causing the issue. For HANS users removal means overwriting the corrupted file with the original. NTR users can just delete them. In general, a crash is likely due to either a bad script or bad dispo file. The first step should be to identify which chapter the crash occurred in and look for its scripts. So if a crash occurred for you in Birthright chapter 6, you'd look for A006.cmb in the Scripts folder and every file that starts with A006 in Scripts->Bev. Remove/Replace these files and try the chapter again. If you still get a crash, follow the same process but remove the dispo file this time. From all of my testing, those were the only files capable of causing full crashes.  If you experience any sort of crash or odd behaviour, feel free to report it in the randomizer thread. I'll do my best to try and fix the issue in a future update.
