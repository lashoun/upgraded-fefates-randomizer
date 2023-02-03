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

By default the randomizer works as explained below. Customizations are possible with the many options provided; if you do not understand, you may also read the code, which should be relatively easy to grasp.

- Each character is given a new total amount of Lvl 1 base stats (by default between 15 and 30) and growth rates (by default between 250 and 350), which are partially randomly distributed, and those stats are scaled back to the level at which they are recruited.
    - For instance, if Ryoma is put in Hinata's recruitment spot (so he will be Lvl 9) and assigned the Archer class, then his stats will be his Lvl 1 stats adjusted with 8 levels of (Ryoma's base growths + Archer class growths);
- Similar to the original randomizer, stats are then shuffled a bit. The default settings are:
    - 10 passes per character, with each pass having:
        - 100% chance of shuffling 5% of growths
        - 50% chance of shuffling 1 stat point
        - 25% chance of shuffling 1 modifier point
- Random swaps of stats / growths / mods can occur (always all three, except for Lck):
    - Str / Mag (default: according to class, 0% chance to swap)
    - Skl / Spd (default: 20% chance to swap)
    - Def / Res (default: according to class, 20% chance to swap)
    - Lck / ? (default: [Lck Growth]% chance, only if Lck stat / growth / mod is superior)
- "Catch 'em all" mode by default: the randomizer will minimize duplicate final classes according to the chosen route (can be disabled with `--disable-class-spread`)
- There is an option to keep all characters at their usual spot but still have the class and stats modifications (option `--disable-model-switch`)
- Minor updates to recruitment levels to make some characters more viable; Hayato joins at Lvl 7 instead of 1 in Birthright, for instance. Can be disabled with `--disable-rebalance-levels`

### Upgraded Fates Features

#### Mods and visuals
- Added the [1.4.0 unofficial update](https://gamebanana.com/mods/51420) of the [Expanded Same-Sex Marriage patch](https://gbatemp.net/threads/fire-emblem-fates-expanded-same-sex-marriage-patch-wip.416109/) by UnassumingVenusaur.
    - Even further: all characters can romantically support one another (fast support type)
- Added Generic Songstress sprite by Moonling
- Nyx has a [witch portrait](https://gamebanana.com/mods/251470)
- Added [FEFates Promotion Texture Patch v.3.2.5](https://moonlingsmodding.tumblr.com/post/185532775066/version-325-update?is_related_post=1): some units will have custom textures for specific classes
    - Added [Azura's Nohrian Songstress outfit](https://gamebanana.com/mods/251475)
- Added [Weapon Model Fix](https://gamebanana.com/mods/51431)
- Added [Unit Select Voice mod](https://gamebanana.com/mods/51423)
- Added [Fates icon project](https://gamebanana.com/mods/34160)
- Added [Gay Paralogue Unlocker](https://gamebanana.com/mods/51421)

#### Chapters
- Changed all "Rout the enemy" objectives to "Defeat the boss"
- Most chapters have a 20-turn limit
- Free Heart Seal given after chapter 5
- Most bosses have been buffed with better weapons
- Endgame chapters of each route should allow the player to save (not tested)
- Birthright Lunatic has been made more difficult: most enemies now have skills
- Birthright Chapter 10 and Revelations Chapter 11 (Ninja village) have one tile changed so that the door is accessible without flier
- Birthright Chapter 11: Reina now spanws on the boat

#### Weapons
- Changes to weapon triangles: Tome <-> Axe, Dagger <-> Sword, and Bow <-> Lance become neutral
    - Rationale: range weapons can already hit melee weapons without retaliation so they shouldn't have weapon advantage on top of that
- Weapon rank requirements decreased by one for every weapon: for instance, iron weapons are available from rank E.
- Weapon updates: increased the difference between Hoshidan and Nohrian weapons, nerfed the hell out of those busted hidden weapons, doubled Staff Exp for convenience. The changes only concern Bronze / Iron / Steel / Silver weapons.
	- Swords, Lances: +1 Mt, -10 Hit, -5 Avo, +2 Crit
	- Katanas, Naginatas: -1 Mt, +5 Hit, +2 Avo
	- Axes: +1 Mt, -10 Hit, -5 Avo
	- Clubs: -1 Mt, +2 Avo, +5 Crit
	- Bows: +1 Mt, -10 Hit, -5 Avo, +2 Crit
	- Yumis: -2 Mt, +10 Hit, +2 Avo
	- Tomes: +1 Mt, -10 Hit, -5 Avo, +2 Crit
	- Scrolls: -1 Mt, +10 Hit, +2 Avo
	- Daggers: -2 Mt, -30 Hit, -5 Avo, +2 Crit, all stat debuffs are decreased by 1
	- Shurikens: -4 Mt, -15 Hit, +5 Avo, +2 Ddg, now give -2 Def, all stat debuffs are decreased by 1
	- Staves: Staff Exp x2 for those listed
		- Heal 10 -> 12 Mt
		- Mend 20 -> 25 Mt
		- Physic 7 -> 9 Mt, range 1-5
		- Recover 35 -> 45 Mt
		- Fortify 7 -> 9 Mt, range 1-5
	- Rod: Staff Exp x2 for those listed
		- Bloom Festal 7 -> 4 Mt
		- Sun Festal 14 -> 10 Mt
		- Wane Festal 2 -> 1 Mt, range 1-12
		- Moon Festal 25 -> 20 Mt
		- Great Festal 2 -> 1 Mt, range 1-12
    - added a *Dragonrune* item: Skill+8, Spd+6, Def-4, Res-3
    - added a *Dragonspell* item: same stats as the Dragonstone, 1-2 range, weak to follow-ups (-5 eff. Spd)
	- Beastrune: Skill-3, Spd-4, Def+5, Res+7 (instead of Skill-2, Spd-1, Def+4, Res+5)
    - added a *Beastspell* item: same stats as the Beaststone, 1-2 range, can't follow-up, weak to follow-ups (-5 eff. Spd)
- Sacred weapons are modified:
    - Raijinto: gives Skl+3 instead of Str+4, range 1
    - Siegfried: gives Def+2 instead of Def+4, range 1
    - Enemy royals have "Sacred weapons+" (Raijinto+/Siegfried+/Fujin Yumi+/Brynhildr+) with buffed Mt (15), and Raijinto+ and Siegfried+ keep 1-2 range and their original buffs (Str/Def +4)
- Wakizashi, Spear, Tomahawk and Battering Club are now 1-2 range, but have -10 Hit and -10 Avo
- All hidden weapons that were not Bronze / Iron / Steel / Silver have -2 Mt and -20 Hit, and all stat debuffs are decreased by 1
- Silver weapons no longer self-debuff, but instead give -10 Avo, -2 Def/Res and -3 eff. Spd in enemy phase
    - Enemies have "Silver Weapons+" which do not have any of the aforementioned maluses
- Beaststones+ and Dragonstones+ now halve Str/Mag until the end of the next fight

#### Characters
- Corrin gets Aptitude, Dragon Fang, Draconic Hex, Nohrian Trust and Hoshidan Unity so you can reclass them immediately after chapter 5; replace Draconic Hex with Nobility if you want the early game to remain interesting

#### Classes
- DLC class gender lock is removed
- All DLC classes except Ballistician are now normal promoted classes
- New class tree (changes are **bolded**):
    Base Class | Class 1 | Class 2
    --- | --- | ---
    Nohr Prince(ss) | Nohr Noble | Hoshido Noble
    Samurai | Swordmaster | **Lodestar**
    Villager | **Great Lord** | Master of Arms
    Apothecary | Merchant | Mechanist |
    Ninja | Master Ninja | **Dread Fighter**
    Oni Savage | Oni Chieftain | Blacksmith
    Spear Fighter | Spear Master | Basara
    Diviner | **Dark Knight** | **Grandmaster**
    Monk | Great Master | Onmyoji
    Shrine Maiden | Priestess | Onmyoji
    Sky Knight | Falcon Knight | **Dark Falcon**
    Archer | Sniper | Kinshi Knight
    Kitsune | Nine-Tails |
    Songstress | |
    Cavalier | Paladin | Great Knight
    Knight | **Warden** | General
    Fighter | Berserker | **Vanguard**
    Mercenary | Hero | Bow Knight
    Outlaw | **Enchanter** | Adventurer
    Wyvern Rider | Wyvern Lord | Malig Knight
    Dark Mage | Sorcerer | **Witch**
    Troubadour | Strategist | Maid/Butler
    Wolfskin | Wolfssegner |
- Detailed class changes:
    - Basara: Quixotic -> Swordbreaker
    - Blacksmith: Salvage Blow -> Death Blow
    - Bow Knight:
        - Bows A->B, Swords B->A
        - Shurikenbreaker -> Galeforce
    - Dark Falcon: Lances B->A, Tomes A->B
    - Dark Knight: Seal Magic -> Luna
    - Diviner: Future Sight -> Solidarity
    - Dread Fighter:
        - Daggers B->A, Swords A->B
        - Clarity -> Iron Will
        - Aggressor -> Tomebreaker
    - Enchanter (new class):
        - Bows A, Tomes B
        - Lvl 5 Sol, Lvl 15 Shurikenbreaker
        -     | HP  | Str | Mag | Skl | Spd | Lck | Def | Res | Mov
          --- | --- | --- | --- | --- | --- | --- | --- | --- |
          Bases | 16 | 6 | 7 | 7 | 7 | 4 | 4 | 5 | 6
          Growths | 0 | 10 | 20 | 10 | 10 | 10 | 0 | 10 | -
          Max Stats | 48 | 29 | 33 | 29 | 31 | 29 | 26 | 30 | -
          Pair Up Bonuses | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | 1
    - Grandmaster: Shurikens ❌->B, Swords B->❌
    - Great Lord: Lances B->A, Swords A->B
    - Lodestar: Speedtaker -> Awakening
    - Master of Arms:
        - Lances B->A, Swords A->B
        - Seal Strength -> Luna
        - Life or Death -> Swordbreaker
    - Mechanist: Daggers A->B, Bow B->A
    - Oni Chieftain: Death Blow -> Rend Heaven, Counter -> Lifetaker
    - Priestess / Great Master: Countermagic -> Inspiration
    - Vanguard:
        - Swords A->B, Axes B->A
        - Strengthtaker -> Lancebreaker
    - Villager:
        - Lances C->B
        - Aptitude -> Dual Striker
        - Underdog -> Charm
    - Warden (new class):
        - Lances A, Daggers B
        - Lvl 5 Savage Blow, Lvl 15 Swordbreaker
        -     | HP  | Str | Mag | Skl | Spd | Lck | Def | Res | Mov
          --- | --- | --- | --- | --- | --- | --- | --- | --- |
          Bases | 20 | 10 | 0 | 9 | 7 | 4 | 9 | 3 | 6 
          Growths | 20 | 15 | 0 | 20 | 10 | 5 | 15 | 0 | -
          Max Stats | 65 | 36 | 25 | 34 | 29 | 32 | 35 | 29 | -
          Pair Up Bonuses | - | 3 | 0 | 3 | 0 | 0 | 2 | 0 | 0
    - Witch:
        - can use Nosferatu innately
        - Warp -> Vengeance
    - Wyvern Lord: Swordbreaker -> Lancebreaker

#### Shops
- Dawn/Dusk armories and Rod/Staff shops available in every route
- Added Dragonstones and Beaststones (-1/-1/-1), Dragonrunes and Beastrunes (0/1/2), Dragonspells and Beastspells (0/1/2) and Dragonstones+ and Beaststones+ (0/0/1), in Rod/Staff shops
- Added 4 Eternal Seals in Shops (4/4/-1) for the retainer replacements, decreased price to 50G
- Most seals now cost 500G
- Seeds of Trust buyable for 10G
- Lvl 2 and 3 shops now appear after chapters 11 and 17 (instead of 13 and 20)
- Most items have had their price decreased
- Overworld RNG weapons (e.g. Raider weapons) are available in shops (0/1/2) for 1500G (the price of steel weapons)

## Instructions

### Requirements

You will need to install [Python](https://www.python.org/), [numpy](https://numpy.org/) and the [xmltodict](https://github.com/martinblech/xmltodict) module. I advise using virtual environments but for the layman a simple
```
pip install numpy xmltodict
```
should do the trick.
The instructions can look daunting but once you understand how it works it takes fewer than 5 minutes to do. Some experience with Python and/or tinkering with files will obviously help though.

0. Begin by either cloning the repository or downloading and extracting the zip.
1. First, choose which version of Fates you want to play (all versions except Vanilla are only compatible with the Special Edition, unfortunately):
    - _Vanilla Fates_: for copyright-related reasons, you will have to dump your own romfs. Follow the instructions in thane89's original readme below.
    - _Gay Fates_: _Vanilla Fates_ patched with vastly expanded supports ([original thread here](https://gbatemp.net/threads/fire-emblem-fates-expanded-same-sex-marriage-patch-wip.416109/)). This is very welcome since randomization doesn't touch supports. Extract `fates_gay_v140_decompressed.7z`.
    - **_Upgraded Gay Fates_ (recommended)**: _Gay Fates_ patched with my curated upgrades listed above. Extract `fates_gay_v140_upgraded_decompressed.7z` and `fates_gay_v140_upgraded_fixed.7z`.
    - _Gay Fates_ (old version): Extract `fates_gay_decompressed.7z`.
    - _Upgraded Gay Fates_ (old version): old _Gay Fates_ patched with the upgrades listed in the Old version paragraph above. Extract `fates_gay_upgraded_decompressed.7z`.
    - _Good Guy Garon Upgraded Gay Fates_: old _Upgraded Gay Fates_ with the [Good Guy Garon Edition patch](https://gbatemp.net/threads/release-conquest-story-overhaul-fire-emblem-fates-good-guy-garon-edition.487117/). Extract `fates_gay_upgraded_GGG_decompressed.7z`.
The extracted `decompressed` folder will be referred to as the `romfs` folder.
2. Run `Fates Randomizer Beta 5-5.jar`, click "Open and Verify", and select the `romfs` folder. You should see a new window pop up with options. If you do not, the window will show you which file was not found. Make sure that the selected folder has folders named `castle`, `GameData`, `m`, `Scripts` directly inside it.
3. Select a path and options. Refer to the [original post](https://gbatemp.net/threads/wip-fire-emblem-fates-randomizer.452268/) if you do not understand an option. I recommend selecting `All Routes` (even if you plan to play Birthright or Conquest, the Python script has route options too) and all options except the experimental ones and the stat randomization.
4. Hit "Randomize" and let the program sit. When the program finishes, a little notification will pop up in the corner of the window.
5. Close `Fates Randomizer Beta 5-5.jar`.
6. Copy the `RandomizerSettings.xml` file from the `romfs` folder to the `data` folder.
7. Open a command prompt in the same folder as `updated_randomizer.py`. Run
```
python updated_randomizer.py
```
  - If you want to know about the options, type:
```
python updated_randomizer.py -h
```
  - Refer to the section "All Options" below for the details.
  - If you did not select the option "Anna" / "Amiibo characters" / "Children" in the randomizer, you have to use the options `-ba` / `-bac` / `-bc` respectively.

8. If the script ran successfully, you should have two files named `RandomizerSettingsUpdated.xml` and `ClassSpread.csv` in the `data` folder. Otherwise, try to run one more time, and if it fails again, raise an issue on this repository.
    - `ClassSpread.csv` contains on each line the original character, their replacement and the class assigned to the replacement. I recommend respecting the file's assignements for more fun and challenge.
    - `RandomizerSettingsUpdated.xml` contains the detailed information of the randomized run. For each character, the `StringData` and `ClassData` fields are tied to the character while the other fields are tied to their spot. If Ryoma has as "switchingCharacter" Hinata, he will have the stats that are written in Hinata's `Stats` field (but those stats will have been computed as Ryoma's "expected" stats at this spot). I recommend not looking at it for more fun.
10. Delete the `romfs` folder and repeat steps 1-5 but, in step 3, choose "Custom Path" and select `RandomizerSettingsUpdated.xml`. Don't forget to check the "Join Order" options again if you did previously.
11. Close `Fates Randomizer Beta 5-5.jar`. Open `FEAT.exe`. Drag the `romfs` folder into FEAT: this will recompress the files. Once FEAT is done, you can close it.
12. Phew! You're done! Now you can copy your `romfs` folder to the mods folder of your gaming medium. If you chose the upgraded version, also copy the content of the `fixed` folder inside the `romfs` folder, and the `exefs` folder to the mods folder.
13. As a final note, DO NOT use this on top of an existing save or branch of fate. Use a fresh save starting from the very beginning if you want a stable playthrough.

## All Available Options
```
usage: updated_randomizer.py [-h] [-ap ADDMAX_POW] [-ab] [-ads] [-ba] [-bac] [-bc] [-bdc] [-bdcs]
                             [-bscap BASE_STAT_CAP] [-bssmax BASE_STATS_SUM_MAX] [-bssmin BASE_STATS_SUM_MIN] [-bw]
                             [-c CORRIN_CLASS] [-dbsr] [-dcd] [-dcs] [-dgd] [-dlts] [-dl] [-dlsc] [-dms] [-drl]
                             [-drlu] [-drr DEF_RES_RATIO] [-drsgs] [-ds] [-dsr] [-dss] [-edbc] [-egd] [-ema] [-emoc]
                             [-epa] [-esc] [-esd] [-esi] [-ev] [-evc] [-g {Revelations,Birthright,Conquest}]
                             [-gc GROWTH_CAP] [-gp GROWTH_P] [-gsmax GROWTHS_SUM_MAX] [-gsmin GROWTHS_SUM_MIN]
                             [-mc MODIFIER_COEFFICIENT] [-mp MOD_P] [-np N_PASSES] [-ns {-1,0,1,2,3,4,5}] [-pmu]
                             [-s SEED] [-sp STAT_P] [-sadp SWAP_ATK_DEF_P] [-sdrp SWAP_DEF_RES_P] [-slp SWAP_LCK_P]
                             [-sssp SWAP_SKL_SPD_P] [-ssmp SWAP_STR_MAG_P] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -ap ADDMAX_POW, --addmax-pow ADDMAX_POW
                        the lower the more uniform growth adjustment
  -ab, --allow-ballistician
                        allow Ballistician class in the randomization
  -ads, --allow-dlc-skills
                        allow DLC skills in skill randomization
  -ba, --ban-anna       ban Anna
  -bac, --ban-amiibo-characters
                        ban Amiibo characters (Marth, Lucina, Robin, Ike)
  -bc, --ban-children   ban children characters
  -bdc, --ban-dlc-classes
                        ban DLC classes
  -bdcs, --ban-dlc-class-skills
                        ban DLC class skills in skill randomization
  -bscap BASE_STAT_CAP, --base-stat-cap BASE_STAT_CAP
                        if adjusting growths, max value for base stat
  -bssmax BASE_STATS_SUM_MAX, --base-stats-sum-max BASE_STATS_SUM_MAX
                        if adjusting growths, decreasing stats sum to that value
  -bssmin BASE_STATS_SUM_MIN, --base-stats-sum-min BASE_STATS_SUM_MIN
                        if adjusting growths, increasing stats sum to that value
  -bw, --ban-witch      ban Witch class from the randomization
  -c CORRIN_CLASS, --corrin-class CORRIN_CLASS
                        Corrin's final class
  -dbsr, --disable-balanced-skill-randomization
                        disable balanced skill randomization; skill randomization will be completely random
  -dcd, --disable-camilla-def
                        disable Camilla's replacement's enforced higher Def than Res
  -dcs, --disable-class-spread
                        disable diverse class reroll
  -dgd, --disable-gunter-def
                        disable Gunter's replacement's enforced higher Def than Res
  -dlts, --disable-livetoserve
                        disable the retainers' replacements' enforced Live to Serve skill
  -dl, --disable-locktouch
                        disable Kaze and Niles' replacements' enforced Locktouch skill
  -dlsc, --disable-limit-staff-classes
                        disables replacing staff only classes by offensive classes and setting the staff only class as
                        a reclass option
  -dms, --disable-model-switch
                        disable model switching but keep switching the rest of the data (stats, growths...)
  -drl, --disable-rebalance-levels
                        disable fairer level balance adjustments (reverts to levels from the original games)
  -drlu, --disable-rng-level-ups
                        disable rng level ups; characters will have average stats w.r.t their growths
  -drr DEF_RES_RATIO, --def-res-ratio DEF_RES_RATIO
                        ratio of higher def/res characters with mixed classes
  -drsgs, --disable-randomize-stats-growths-sum
                        will disable randomizing stats and growths sum for each character between customizable bounds
  -ds, --disable-songstress
                        disable Azura's replacement's enforced Songstress class
  -dsr, --disable-staff-retainer
                        disable Jakob and Felicia's replacement's enforced healing class
  -dss, --disable-staff-early-recruit
                        disable Sakura and/or Elise's replacement's enforced healing class
  -edbc, --enable-dlc-base-class
                        will give unpromoted base classes to every DLC class for game balance (eg Ninja/Oni Savage for
                        Dread Fighter)
  -egd, --enable-genderless-dlc
                        allows DLC classes to be given regardless of gender. Will automatically trigger --enable-dlc-
                        base-class since this will affect only unpromoted characters; prepromoted characters are
                        banned from getting an illegal class since the randomizer doesn't support it
  -ema, --enforce-mozu-aptitude
                        enforce Mozu (herself) having Aptitude
  -emoc, --enable-mag-only-corrin
                        enables Corrin to get a Mag only class
  -epa, --enforce-paralogue-aptitude
                        enforce Mozu's replacement to have Aptitude
  -esc, --enforce-sword-corrin
                        enforces Corrin to get a sword-wielding final class
  -esd, --enforce-stat-decrease
                        enforces stat decrease to base stat sum max regardless of growth increase
  -esi, --enforce-stat-increase
                        enforces stat increase to base stat sum min
  -ev, --enforce-villager
                        enforce Mozu's replacement being a Villager with Aptitude
  -evc, --enforce-viable-characters
                        will force you to play with only the first 15 characters encoutered by giving 0 growth rates
                        to the others in the route; non-iable characters will be given the 'Survey' skill for easy
                        identification
  -g {Revelations,Birthright,Conquest}, --game-route {Revelations,Birthright,Conquest}
                        game route, especially important to specify it if playing Revelations so that levels are the
                        correct ones
  -gc GROWTH_CAP, --growth-cap GROWTH_CAP
                        adjusted growths cap
  -gp GROWTH_P, --growth-p GROWTH_P
                        probability of editing growths in a variability pass
  -gsmax GROWTHS_SUM_MAX, --growths-sum-max GROWTHS_SUM_MAX
                        will adjust growths until sum is lower than specified value
  -gsmin GROWTHS_SUM_MIN, --growths-sum-min GROWTHS_SUM_MIN
                        will adjust growths until sum is higher than specified value
  -mc MODIFIER_COEFFICIENT, --modifier-coefficient MODIFIER_COEFFICIENT
                        will increase all modifiers by specified coefficient
  -mp MOD_P, --mod-p MOD_P
                        probability of editing modifiers in a variability pass
  -np N_PASSES, --n-passes N_PASSES
                        number of variability passes (swap +/- 5 growths, +/- 1 stats and mods per pass
  -ns {-1,0,1,2,3,4,5}, --n-skills {-1,0,1,2,3,4,5}
                        number of randomized skills; if -1, randomize existing skills
  -pmu, --pmu-mode      `ClassSpread.csv` will only contain the 16 allowed characters for the run
  -s SEED, --seed SEED  RNG seed
  -sp STAT_P, --stat-p STAT_P
                        probability of editing stats in a variability pass
  -sadp SWAP_ATK_DEF_P, --swap-atk-def-p SWAP_ATK_DEF_P
                        probability of swapping Str/Mag (higher one) with Def/Res (higher one) growths / stats /
                        modifiers
  -sdrp SWAP_DEF_RES_P, --swap-def-res-p SWAP_DEF_RES_P
                        probability of swapping Def and Res growths / stats / modifiers
  -slp SWAP_LCK_P, --swap-lck-p SWAP_LCK_P
                        probability of swapping Lck and a random stat's growths / stats / modifiers; random if between
                        0 and 1, else [(Lck Growth)% and swap only if Lck is superior]
  -sssp SWAP_SKL_SPD_P, --swap-skl-spd-p SWAP_SKL_SPD_P
                        probability of swapping Skl and Spd growths / stats / modifiers
  -ssmp SWAP_STR_MAG_P, --swap-str-mag-p SWAP_STR_MAG_P
                        probability of swapping Str and Mag growths / stats / modifiers; random if between 0 and 1,
                        else according to class (coin flip for mixed classes)
  -v, --verbose         print verbose stuff
```

### Example Custom Run
```
python updated_randomizer.py -bssmax 27 -bssmin 18 -edbc -egd -elsc -epa -esc -g "Conquest" -gsmax 350 -gsmin 300 -mc 5 -ns 4
```

This example command will ensure the following:
- all units will have a total Lvl 1 base stats sum randomly sampled between 18 and 27
- non-promoted units who are assigned a DLC class will get a fitting base class
- DLC classes will not be gender-locked, but it might cause the randomizer to fail if a prepromoted unit gets a "wrong" DLC class
- there will only be 2 staff-only characters (the retainer and an early recruit)
- Mozu's replacement will have Aptitude
- Corrin will have a sword-wielding final class
- only Conquest replacement units will be updated; in particular, they should all have different final classes (except maybe children).
- all units will have a total growth rates sum randomly sampled between 300 and 350
- all unit stat modifiers will be increased by 5
- all units will have 4 randomized skills

## Troubleshooting

### Chapter 2: There's an immobile "phantom" unit near the top left corner!
This sometimes happens. Just kill it after the others, you should be able to.

### Chapter 5: This chapter is way too hard!
I advise using the Infinite Movement cheat code for this chapter. If you can play Randomized Fates, you can probably find how to use cheats on your gaming medium.

### Conquest Chapter 9: Talking with Nyx crashes the game!
Break the wall near Nyx before talking to her. 

### Conquest Chapter 16: The game freezes after the "Spare Shura" prompt!
You need to rename or delete the file `Scripts/B/B016.cmb`. This might skip the prompt in its entirety, meaning you won't get anything, but at least you can play the rest of the route.

### Revelations Chapter 8: Hayato was not replaced!
This is an issue from the original randomizer; I can't fix it myself. This can amusingly lead to recruiting two Hayatos.

### Revelations Chapter 13: The obstacles are invisible!
This is a known issue. No fix for this at the moment.
