# -*- coding: utf-8 -*-

import xmltodict
import csv
import numpy as np
import argparse
from numpy.random import default_rng


## Initialize path and arguments

path = './data'

parser = argparse.ArgumentParser()
parser.add_argument('-ap', '--addmax-pow', type=float, default=1., help="the lower the more uniform growth adjustment")
parser.add_argument('-ab', '--allow-ballistician', action='store_true', help="allow Ballistician class in the randomization")
parser.add_argument('-ba', '--ban-anna', action='store_true', help="ban Anna")
parser.add_argument('-bac', '--ban-amiibo-characters', action='store_true', help="ban Amiibo characters (Marth, Lucina, Robin, Ike)")
parser.add_argument('-bc', '--ban-children', action='store_true', help="ban children characters")
parser.add_argument('-bdc', '--ban-dlc-classes', action='store_true', help="ban DLC classes")
parser.add_argument('-bss', '--base-stats-sum', type=int, default=25, help="if adjusting growths, lowering stats sum to that value")
parser.add_argument('-bw', '--ban-witch', action='store_true', help="ban Witch class from the randomization")
parser.add_argument('-c', '--corrin-class', choices=[
    'Hoshido Noble', 'Swordmaster', 'Master of Arms', 'Oni Chieftain',
    'Blacksmith', 'Spear Master', 'Basara', 'Onmyoji', 'Great Master',
    'Priestess', 'Falcon Knight', 'Kinshi Knight', 'Sniper',
    'Master Ninja', 'Mechanist', 'Merchant', 'Nine-Tails', 'Nohr Noble',
    'Paladin', 'Great Knight', 'General', 'Berserker', 'Hero',
    'Bow Knight', 'Adventurer', 'Wyvern Lord', 'Malig Knight',
    'Sorcerer', 'Dark Knight', 'Strategist', 'Maid', 'Butler',
    'Wolfssegner', 'Songstress', 'Dread Fighter', 'Dark Falcon',
    'Ballistician', 'Witch', 'Lodestar', 'Vanguard', 'Great Lord', 'Grandmaster'
],
                    default='', help="Corrin's final class", metavar="CORRIN_CLASS")
parser.add_argument('-dcs', '--disable-class-spread', action='store_true', help="disable diverse class reroll")
parser.add_argument('-dgd', '--disable-gunter-def', action='store_true', help="disable Gunter's replacement's enforced higher Def than Res")
parser.add_argument('-dl', '--disable-locktouch', action='store_true', help="disable Kaze's replacement's enforced Locktouch skill")
parser.add_argument('-dms', '--disable-model-switch', action='store_true', help="disable model switching but keep switching the rest of the data (stats, growths...)")
parser.add_argument('-ds', '--disable-songstress', action='store_true', help="disable Azura's replacement's enforced Songstress class")
parser.add_argument('-dsr', '--disable-staff-retainer', action='store_true', help="disable Jakob and Felicia's replacement's enforced healing class")
parser.add_argument('-dss', '--disable-staff-sister', action='store_true', help="disable Sakura and/or Elise's replacement's enforced healing class")
parser.add_argument('-ema', '--enforce-mozu-aptitude', action='store_true', help="enforce Mozu (herself) having Aptitude")
parser.add_argument('-emoc', '--enable-mag-only-corrin', action='store_true', help="enables Corrin to get a Mag only class")
parser.add_argument('-esc', '--enforce-sword-corrin', action='store_true', help="enforces Corrin to get a sword-wielding final class")
parser.add_argument('-esd', '--enforce-stat-decrease', action='store_true', help="enforces stat decrease regardless of growth increase")
parser.add_argument('-esi', '--enforce-stat-increase', action='store_true', help="enforces stat increase")
parser.add_argument('-ev', '--enforce-villager', action='store_true', help="enforce Mozu's replacement being a Villager with Aptitude")
parser.add_argument('-g', '--game-route', choices=['Revelations', 'Birthright', 'Conquest'],
                    default='Revelations', help="game route")
parser.add_argument('-gc', '--growth-cap', type=int, default=70, help="adjusted growths cap")
parser.add_argument('-gp', '--growth-p', type=float, default=1., help="probability of editing growths in a variability pass")
parser.add_argument('-gsm', '--growths-sum-min', type=int, default=270, help="will adjust grwoths until sum is higher than specified value")
parser.add_argument('-mc', '--modifier-coefficient', type=int, default=0, help="will increase all modifiers by specified coefficient")
parser.add_argument('-mp', '--mod-p', type=float, default=0.25, help="probability of editing modifiers in a variability pass")
parser.add_argument('-np', '--n-passes', type=int, default=10, help="number of variability passes (swap +/- 5 growths, +/- 1 stats and mods per pass")
parser.add_argument('-ns', '--n-skills', type=int, default=-1, choices=[-1, 0, 1, 2, 3, 4, 5], help="number of randomized skills; if -1, randomize existing skills")
parser.add_argument('-s', '--seed', type=int, default=None, help="RNG seed")
parser.add_argument('-sp', '--stat-p', type=float, default=0.5, help="probability of editing stats in a variability pass")
parser.add_argument('-sdrp', '--swap-def-res-p', type=float, default=0.2, help="probability of swapping Def and Res growths / stats / modifiers")
parser.add_argument('-slp', '--swap-lck-p', type=float, default=-1., help="probability of swapping Lck and a random stat's growths / stats / modifiers; random if between 0 and 1, else [(Lck Growth)%% and swap only if Lck is superior]")
parser.add_argument('-sssp', '--swap-skl-spd-p', type=float, default=0.2, help="probability of swapping Skl and Spd growths / stats / modifiers")
parser.add_argument('-ssmp', '--swap-str-mag-p', type=float, default=-1., help="probability of swapping Str and Mag growths / stats / modifiers; random if between 0 and 1, else according to class (coin flip for mixed classes)")
parser.add_argument('-v', '--verbose', action='store_true', help="print verbose stuff")
args = parser.parse_args()


## Load data

with open('{}/fates_data_hub.csv'.format(path)) as fcsv:
    reader = csv.reader(fcsv, quoting=csv.QUOTE_NONNUMERIC)
    allCharacterData = {}
    next(reader)  # skip first row
    for row in reader:
        name = row[0]
        stats = list(map(int, row[1:9]))
        growths = list(map(int, row[9:17]))
        modifiers = list(map(int, row[17:25]))
        baseStats = list(map(int, row[25:33]))
        level = int(row[33])
        baseStatsTotal = int(row[34])
        growthsTotal = int(row[35])
        promotionLevel = int(row[36])
        originalClass = row[37]
        baseClass = row[38]
        allCharacterData[name] = {
            'Stats': stats,
            'Growths': growths,
            'Modifiers': modifiers,
            'BaseStats': baseStats,
            'Level': level,
            'Name': name,
            'BaseStatsTotal': baseStatsTotal,
            'GrowthsTotal': growthsTotal,
            'PromotionLevel': promotionLevel,
            'OriginalClass': originalClass,
            'BaseClass': baseClass
        }


with open('{}/fates_class_data.csv'.format(path)) as fcsv:
    reader = csv.reader(fcsv)
    classData = {}
    next(reader)
    for row in reader:
        baseClasses = row[10:12]
        while len(baseClasses) > 0:
            if baseClasses[-1] == '':
                baseClasses.pop()
            else:
                break
        classData[row[0]] = {
            'AttackType': row[1],
            'Growths': list(map(int, row[2:10])),
            'BaseClasses': baseClasses
        }


with open('{}/RandomizerSettings.xml'.format(path)) as fxml:
    settings = xmltodict.parse(fxml.read())


## Randomizer Class

class FatesRandomizer:
    def __init__(
        self,
        allCharacterData,
        classData,
        settings,
        addmaxPow=1,
        banAmiiboCharacters=False,
        banAnna=False,
        banBallistician=True,
        banChildren=False,
        banDLCClasses=False,
        banWitch=False,
        baseStatsSumMax=25,  # in adjustBaseStatsAndGrowths, if growths have to be increased, will decrease stats sum to said value
        corrinClass='',
        disableModelSwitch=False,  # will disable model switching
        forceClassSpread=True,  # will limit class duplicates
        forceGunterDef=True,  # will force Gunter's replacement to have higher Def
        forceLocktouch=True,  # will force Kaze's replacement to get Locktouch
        forceMozuAptitude=False,  # will force Mozu (not her replacement) to get Aptitude
        forceStaffRetainer=True,  # will force the retainer's replacement to get a promoted class with a staff
        forceStaffSister=True,  # will force the little sister's replacement (Sakura in BR or RV / Elise in CQ) to get a healing class
        forceStatDecrease=False,  # force stat decrase in adjustBaseStatsAndGrowths
        forceStatIncrease=False,  # force stat increase in adjustBaseStatsAndGrowths
        forceSongstress=True,  # will force Azura's replacement to be a Songstress
        forceStrCorrin=True,  # will force Corrin to have a class that wields at least one Str weapon
        forceSwordCorrin=False,  # will force Corrin to have a class that wields swords
        # TODO: forceViableCharacters=True,  # will choose 15 non-children characters for each route, others will have no skills and 0 growths everywhere
        forceVillager=False,  # will force Mozu's replacement to be a Villager and get Aptitude
        gameRoute='Revelations',  # 'Birthright', 'Conquest' or 'Revelations', used in randomizeClasses
        growthCap=70,  # growth cap in adjustBaseStatsAndGrowths
        growthP=1,  # proba of editing growths in AddVariancetoData
        growthsSumMin=270,  # in adjustBaseStatsAndGrowths, will increase growths sum up to said value
        modifierCoefficient=0,  # value by which all modifiers will be increased
        modP=0.25,  # proba of editing modifiers in AddVariancetoData
        nPasses=10,  # number of passes in AddVariancetoData
        nSkills=-1,  # if -1, randomize existing skills
        seed=None,
        statP=0.5,  # proba of editing stats in AddVariancetoData
        swapDefResP=0.2,  # random
        swapLckP=-1, # random if between 0 and 1, else [(Lck Growth)% and only swap if Lck is superior]
        swapSklSpdP=0.2,  # random
        swapStrMagP=-1,  # random if between 0 and 1, else according to class
        verbose=False
    ):
        self.allCharacterData = allCharacterData.copy()
        self.classData = classData.copy()
        self.settings = settings.copy()

        assert nSkills <= 5, "nSkills must be <= 5"

        self.addmaxPow = addmaxPow
        self.banAmiiboCharacters = banAmiiboCharacters
        self.banAnna = banAnna
        self.banChildren = banChildren
        self.banBallistician = banBallistician
        self.banDLCClasses = banDLCClasses
        self.banWitch = banWitch
        self.baseStatsSumMax = baseStatsSumMax
        self.corrinClass = corrinClass
        self.disableModelSwitch = disableModelSwitch
        self.forceClassSpread = forceClassSpread
        self.forceGunterDef = forceGunterDef
        self.forceLocktouch = forceLocktouch
        self.forceMozuAptitude = forceMozuAptitude
        self.forceStaffRetainer = forceStaffRetainer
        self.forceStaffSister = forceStaffSister
        self.forceStatDecrease = forceStatDecrease
        self.forceStatIncrease = forceStatIncrease
        self.forceSongstress = forceSongstress
        self.forceStrCorrin = forceStrCorrin
        self.forceSwordCorrin = forceSwordCorrin
        self.forceVillager = forceVillager
        self.gameRoute = gameRoute
        self.growthCap = growthCap
        self.growthP = growthP
        self.growthsSumMin = growthsSumMin
        self.modifierCoefficient = modifierCoefficient
        self.modP = modP
        self.nPasses = nPasses
        self.nSkills = nSkills
        self.rng = default_rng(seed)
        self.statP = statP
        self.swapDefResP = swapDefResP
        self.swapLckP = swapLckP
        self.swapSklSpdP = swapSklSpdP
        self.swapStrMagP = swapStrMagP
        self.verbose=verbose

        self.BEAST_CLASSES = ['Wolfskin', 'Wolfssegner', 'Kitsune', 'Nine-Tails']
        self.DRAGON_CLASSES = ['Nohr Prince', 'Nohr Princess', 'Nohr Noble', 'Hoshido Noble']

        self.FELICIA_CLASSES = ['Hoshido Noble', 'Onmyoji', 'Priestess',
                                'Falcon Knight', 'Adventurer', 'Strategist', 'Maid']
        self.JAKOB_CLASSES = ['Hoshido Noble', 'Onmyoji', 'Great Master',
                              'Falcon Knight', 'Adventurer', 'Strategist', 'Butler']
        self.SISTER_CLASS = ['Onmyoji', 'Priestess', 'Strategist', 'Maid']

        self.MALE_CLASSES = ['Great Master', 'Butler', 'Lodestar', 'Vanguard', 'Grandmaster', 'Ballistician']
        self.FEMALE_CLASSES = ['Priestess', 'Maid', 'Witch', 'Great Lord']

        self.DLC_CLASSES = ['Dread Fighter', 'Dark Falcon', 'Ballistician',
            'Witch', 'Lodestar', 'Vanguard', 'Great Lord', 'Grandmaster']

        self.FINAL_CLASSES = [
            'Hoshido Noble', 'Swordmaster', 'Master of Arms', 'Oni Chieftain',
            'Blacksmith', 'Spear Master', 'Basara', 'Onmyoji', 'Great Master',
            'Priestess', 'Falcon Knight', 'Kinshi Knight', 'Sniper',
            'Master Ninja', 'Mechanist', 'Merchant', 'Nine-Tails', 'Nohr Noble',
            'Paladin', 'Great Knight', 'General', 'Berserker', 'Hero',
            'Bow Knight', 'Adventurer', 'Wyvern Lord', 'Malig Knight',
            'Sorcerer', 'Dark Knight', 'Strategist', 'Maid', 'Butler',
            'Wolfssegner', 'Songstress', 'Dread Fighter', 'Dark Falcon',
            'Ballistician', 'Witch', 'Lodestar', 'Vanguard', 'Great Lord', 'Grandmaster'
        ]
        self.MAGICAL_CLASSES = [
            'Onmyoji', 'Sorcerer', 'Strategist', 'Witch'
        ]
        self.SWORD_CLASSES = [
            'Hoshido Noble', 'Swordmaster', 'Master of Arms', 'Blacksmith',
            'Master Ninja', 'Nohr Noble', 'Paladin', 'Great Knight', 'Hero',
            'Bow Knight', 'Dark Knight', 'Dread Fighter', 'Lodestar',
            'Vanguard', 'Great Lord', 'Grandmaster'
        ]
        self.PROMOTED_CLASSES = [
            'Hoshido Noble', 'Swordmaster', 'Master of Arms', 'Oni Chieftain',
            'Blacksmith', 'Spear Master', 'Basara', 'Onmyoji', 'Great Master',
            'Priestess', 'Falcon Knight', 'Kinshi Knight', 'Sniper', 'Master Ninja',
            'Mechanist', 'Merchant', 'Nine-Tails', 'Nohr Noble', 'Paladin',
            'Great Knight', 'General', 'Berserker', 'Hero', 'Bow Knight',
            'Adventurer', 'Wyvern Lord', 'Malig Knight', 'Sorcerer', 'Dark Knight',
            'Strategist', 'Maid', 'Butler', 'Wolfssegner'
        ]
        self.UNPROMOTED_CLASSES = [
            'Samurai', 'Oni Savage', 'Spear Fighter', 'Diviner', 'Shrine Maiden',
            'Monk', 'Sky Knight', 'Archer', 'Ninja', 'Apothecary', 'Kitsune',
            'Songstress', 'Villager', 'Nohr Prince', 'Nohr Princess', 'Cavalier',
            'Knight', 'Fighter', 'Mercenary', 'Outlaw', 'Wyvern Rider', 'Dark Mage',
            'Troubadour', 'Wolfskin', 'Dread Fighter', 'Dark Falcon', 'Ballistician',
            'Witch', 'Lodestar', 'Vanguard', 'Great Lord', 'Grandmaster'
        ]

        self.AMIIBO_CHARACTERS = ['Marth', 'Lucina', 'Robin', 'Ike']

        self.BIRTHRIGHT_CHARACTERS = [
            'Felicia', 'Jakob', 'Kaze', 'Rinkah', 'Azura', 'Sakura', 'Hana', 'Subaki',
            'Silas', 'Saizo', 'Orochi', 'Anna', 'Mozu', 'Hinoka', 'Azama', 'Setsuna',
            'Hayato', 'Oboro', 'Hinata', 'Takumi', 'Kagero', 'Reina', 'Kaden', 'Ryoma',
            'Scarlet', 'Izana', 'Shura', 'Yukimura', 'Shigure', 'Dwyer', 'Sophie',
            'Midori', 'Shiro', 'Kiragi', 'Asugi', 'Selkie', 'Hisame', 'Mitama', 'Caeldori',
            'Rhajat', 'Marth', 'Lucina', 'Robin', 'Ike'
        ]
        self.CONQUEST_CHARACTERS = [
            'Felicia', 'Jakob', 'Elise', 'Silas', 'Arthur', 'Effie', 'Anna', 'Mozu',
            'Odin', 'Niles', 'Azura', 'Nyx', 'Camilla', 'Selena', 'Beruka', 'Kaze',
            'Laslow', 'Peri', 'Benny', 'Charlotte', 'Leo', 'Keaton', 'Gunter',
            'Xander', 'Shura', 'Flora', 'Izana', 'Shigure', 'Dwyer', 'Sophie',
            'Midori', 'Siegbert', 'Forrest', 'Ignatius', 'Velouria', 'Percy',
            'Ophelia', 'Soleil', 'Nina', 'Marth', 'Lucina', 'Robin', 'Ike',
        ]
        self.REVELATION_CHARACTERS = [
            'Azura', 'Felicia', 'Jakob', 'Gunter', 'Anna', 'Mozu', 'Sakura', 'Hana',
            'Subaki', 'Kaze', 'Rinkah', 'Hayato', 'Takumi', 'Oboro', 'Hinata',
            'Saizo', 'Orochi', 'Reina', 'Kagero', 'Camilla', 'Selena', 'Beruka',
            'Kaden', 'Keaton', 'Elise', 'Arthur', 'Effie', 'Charlotte', 'Benny',
            'Silas', 'Shura', 'Nyx', 'Hinoka', 'Azama', 'Setsuna', 'Ryoma',
            'Scarlet', 'Leo', 'Xander', 'Odin', 'Niles', 'Laslow', 'Peri',
            'Flora', 'Fuga', 'Shigure', 'Dwyer', 'Sophie', 'Midori', 'Shiro',
            'Kiragi', 'Asugi', 'Selkie', 'Hisame', 'Mitama', 'Caeldori', 'Rhajat',
            'Siegbert', 'Forrest', 'Ignatius', 'Velouria', 'Percy', 'Ophelia',
            'Soleil', 'Nina', 'Marth', 'Lucina', 'Robin', 'Ike'
        ]

        self.CHILDREN_CHARACTERS = ['Shigure', 'Dwyer', 'Sophie', 'Midori', 'Shiro',
            'Kiragi', 'Asugi', 'Selkie', 'Hisame', 'Mitama', 'Caeldori', 'Rhajat',
            'Siegbert', 'Forrest', 'Ignatius', 'Velouria', 'Percy', 'Ophelia',
            'Soleil', 'Nina']

        self.MALE_CHARACTERS = [
            'Jakob', 'Fuga', 'Yukimura', 'Izana', 'Subaki', 'Kaze', 'Hayato',
            'Takumi', 'Hinata', 'Saizo', 'Kaden', 'Keaton', 'Arthur', 'Benny',
            'Silas', 'Shura', 'Azama', 'Ryoma', 'Leo', 'Odin', 'Niles',
            'Xander', 'Laslow', 'Gunter', 'Marth', 'Robin', 'Ike', 'Shigure',
            'Dwyer', 'Shiro', 'Kiragi', 'Asugi', 'Hisame', 'Siegbert',
            'Forrest', 'Ignatius', 'Percy'
        ]
        self.FEMALE_CHARACTERS = ['Felicia', 'Flora', 'Azura', 'Hana', 'Sakura',
            'Rinkah', 'Oboro', 'Orochi', 'Reina', 'Kagero', 'Camilla', 'Selena',
            'Beruka', 'Elise', 'Effie', 'Charlotte', 'Nyx', 'Hinoka', 'Setsuna',
            'Scarlet', 'Peri', 'Mozu', 'Anna', 'Lucina', 'Sophie', 'Midori',
            'Selkie', 'Mitama', 'Caeldori', 'Rhajat', 'Velouria', 'Ophelia',
            'Soleil', 'Nina'
        ]
        self.ROYALS = ['Azura', 'Sakura', 'Hinoka', 'Elise', 'Camilla', 'Takumi',
                       'Ryoma', 'Leo', 'Xander']

        self.randomizedClasses = None

        if self.banAmiiboCharacters:
            for characterName in self.AMIIBO_CHARACTERS:
                if characterName != 'Lucina':
                    self.MALE_CHARACTERS.pop(self.MALE_CHARACTERS.index(characterName))
                else:
                    self.FEMALE_CHARACTERS.pop(self.FEMALE_CHARACTERS.index(characterName))
                self.BIRTHRIGHT_CHARACTERS.pop(self.BIRTHRIGHT_CHARACTERS.index(characterName))
                self.CONQUEST_CHARACTERS.pop(self.CONQUEST_CHARACTERS.index(characterName))
                self.REVELATION_CHARACTERS.pop(self.REVELATION_CHARACTERS.index(characterName))
        if self.banAnna:
            self.FEMALE_CHARACTERS.pop(self.FEMALE_CHARACTERS.index('Anna'))
            self.BIRTHRIGHT_CHARACTERS.pop(self.BIRTHRIGHT_CHARACTERS.index('Anna'))
            self.CONQUEST_CHARACTERS.pop(self.CONQUEST_CHARACTERS.index('Anna'))
            self.REVELATION_CHARACTERS.pop(self.REVELATION_CHARACTERS.index('Anna'))
        if self.banChildren:
            for characterName in self.CHILDREN_CHARACTERS:
                if characterName in self.MALE_CHARACTERS:
                    self.MALE_CHARACTERS.pop(self.MALE_CHARACTERS.index(characterName))
                if characterName in self.FEMALE_CHARACTERS:
                    self.FEMALE_CHARACTERS.pop(self.FEMALE_CHARACTERS.index(characterName))
                if characterName in self.BIRTHRIGHT_CHARACTERS:
                    self.BIRTHRIGHT_CHARACTERS.pop(self.BIRTHRIGHT_CHARACTERS.index(characterName))
                if characterName in self.CONQUEST_CHARACTERS:
                    self.CONQUEST_CHARACTERS.pop(self.CONQUEST_CHARACTERS.index(characterName))
                self.REVELATION_CHARACTERS.pop(self.REVELATION_CHARACTERS.index(characterName))

        if self.banDLCClasses:
            for className in self.DLC_CLASSES:
                if className in self.MALE_CLASSES:
                    self.MALE_CLASSES.pop(self.MALE_CLASSES.index(className))
                if className in self.FEMALE_CLASSES:
                    self.FEMALE_CLASSES.pop(self.FEMALE_CLASSES.index(className))
                self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index(className))
                self.UNPROMOTED_CLASSES.pop(self.UNPROMOTED_CLASSES.index(className))
                if className in self.MAGICAL_CLASSES:
                    self.MAGICAL_CLASSES.pop(self.MAGICAL_CLASSES.index(className))
                if className in self.SWORD_CLASSES:
                    self.SWORD_CLASSES.pop(self.SWORD_CLASSES.index(className))
        else:
            if self.banBallistician:
                self.MALE_CLASSES.pop(self.MALE_CLASSES.index('Ballistician'))
                self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index('Ballistician'))
                self.UNPROMOTED_CLASSES.pop(self.UNPROMOTED_CLASSES.index('Ballistician'))
            if self.banWitch:
                self.FEMALE_CLASSES.pop(self.FEMALE_CLASSES.index('Witch'))
                self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index('Witch'))
                self.UNPROMOTED_CLASSES.pop(self.UNPROMOTED_CLASSES.index('Witch'))
                self.MAGICAL_CLASSES.pop(self.MAGICAL_CLASSES.index('Witch'))

        if self.gameRoute == 'Birthright':
            self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index('Nohr Noble'))
            self.PROMOTED_CLASSES.pop(self.PROMOTED_CLASSES.index('Nohr Noble'))
            self.SWORD_CLASSES.pop(self.SWORD_CLASSES.index('Nohr Noble'))
        elif self.gameRoute == 'Conquest':
            self.JAKOB_CLASSES.pop(self.JAKOB_CLASSES.index('Hoshido Noble'))
            self.FELICIA_CLASSES.pop(self.FELICIA_CLASSES.index('Hoshido Noble'))
            self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index('Hoshido Noble'))
            self.PROMOTED_CLASSES.pop(self.PROMOTED_CLASSES.index('Hoshido Noble'))
            self.SWORD_CLASSES.pop(self.SWORD_CLASSES.index('Hoshido Noble'))

        if self.forceClassSpread:
            self.randomizeAllClasses()

    def addmax(self, x):
        p = self.addmaxPow
        x = x**p
        return x / np.sum(x)

    def addVarianceToData(self, stats, growths, mods):
        """ Takes points from a given stat / growth / modifier and gives it to another """
        for _ in range(self.nPasses):
            i, j = self.rng.choice(8, 2, replace=False)
            x = self.rng.random()
            if x < self.growthP:
                if growths[j] >= 5 and growths[i] <= self.growthCap:
                    growths[i] += 5
                    growths[j] -= 5
            if x < self.statP:
                if stats[j] >= 1:
                    stats[i] += 1
                    stats[j] -= 1
            if x < self.modP:
                mods[i] += 1
                mods[j] -= 1
        return growths, stats, mods

    def adjustBaseStatsAndGrowths(self, characterData):
        """
        - If the character's growths are too low (e.g. Fuga, Gunter), raise
        them up to a total sum of `self.growthsSumMin`.
        - In counterpart, if growths are increased, decrease base stats down
        to a total sum of `self.baseStatsSumMax`.
        """
        growths = np.copy(characterData['Growths'])
        baseStats = np.copy(characterData['BaseStats'])
        growthsSum = np.sum(growths)
        baseStatsSum = np.sum(baseStats)
        probas = self.addmax(np.asarray(growths) + 5)  # add a 5 growth rate to everything
        if growthsSum < self.growthsSumMin or self.forceStatDecrease:
            while growthsSum < self.growthsSumMin:
                s = self.rng.choice(8, p=probas)
                if growths[s] < self.growthCap:
                    growths[s] += 5
                    growthsSum += 5
                else:
                    probas[s] = 0
                    probas = self.addmax(probas)
            while baseStatsSum > self.baseStatsSumMax:
                t = self.rng.choice(np.where(baseStats>0)[0])
                baseStats[t] -= 1
                baseStatsSum -= 1
        if self.forceStatIncrease:
            while baseStatsSum < self.baseStatsSumMax:
                t = self.rng.choice(8, p=probas)
                baseStats[t] += 1
                baseStatsSum += 1
        characterData['Growths'] = growths
        characterData['BaseStats'] = baseStats
        return characterData

    def checkGender(self, characters, classes):
        """ in place """
        genderCheck = False
        while not genderCheck:
            genderCheck = True
            for i, className in enumerate(classes):
                character = characters[i]
                if className in self.MALE_CLASSES:
                    if character not in self.MALE_CHARACTERS:
                        newCharacter = self.rng.choice(self.MALE_CHARACTERS)
                        while newCharacter not in characters:
                            newCharacter = self.rng.choice(self.MALE_CHARACTERS)
                        j = characters.index(newCharacter)
                        classes[i], classes[j] = classes[j], classes[i]
                        genderCheck = False
                if className in self.FEMALE_CLASSES:
                    if character not in self.FEMALE_CHARACTERS:
                        newCharacter = self.rng.choice(self.FEMALE_CHARACTERS)
                        while newCharacter not in characters:
                            newCharacter = self.rng.choice(self.FEMALE_CHARACTERS)
                        j = characters.index(newCharacter)
                        classes[i], classes[j] = classes[j], classes[i]
                        genderCheck = False
        return characters, classes

    def computeBaseStats(self, characterName):
        """ returns the lvl 1 stats of the character """

        characterStats = self.readCharacterStats(characterName)
        characterGrowths = self.readCharacterGrowths(characterName)

        level = self.readCharacterLevel(characterName)
        promotionLevel = self.readCharacterPromotionLevel(characterName)
        baseClass = self.readCharacterBaseClass(characterName)
        originalClass = self.readCharacterOriginalClass(characterName)
        baseClassGrowths = self.readClassGrowths(baseClass)
        originalClassGrowths = self.readClassGrowths(originalClass)

        minusStats = np.zeros(8)
        if level > 1:
            minusStats += (characterGrowths + originalClassGrowths) * (level - 1)
        if promotionLevel > 1:
            minusStats += (characterGrowths + baseClassGrowths) * (promotionLevel - 1)
        minusStats = np.floor(minusStats/100)

        characterBaseStats = characterStats - minusStats

        return characterBaseStats

    def computeNewStats(self, character):
        """ Returns the new stats of the character: base stats are
        scaled up to the new level with the new class growths """

        characterName = self.readCharacterName(character)
        characterBaseStats = self.readCharacterBaseStats(characterName)
        characterGrowths = self.readCharacterGrowths(characterName)

        switchingCharacterName = self.readSwitchingCharacterName(character)
        switchingCharacter = self.getCharacter(switchingCharacterName)

        newLevel = self.readCharacterLevel(switchingCharacterName)
        newPromotionLevel = self.readCharacterPromotionLevel(switchingCharacterName)
        newClass = self.readClassName(character)
        newBaseClass = self.readBaseClass(newClass, characterName)
        newClassGrowths = self.readClassGrowths(newClass)
        newBaseClassGrowths = self.readClassGrowths(newBaseClass)

        plusStats = np.zeros(8)
        if newLevel > 1:
            plusStats += (characterGrowths + newClassGrowths) * (newLevel - 1)
        if promotionLevel > 1:
            plusStats += (characterGrowths + newBaseClassGrowths) * (newPromotionLevel - 1)
        plusStats = np.floor(plusStats/100)

        characterNewStats = characterBaseStats + plusStats

        return characterNewStats

    def dataToString(self, data):
        return ','.join(list(map(str, list(map(int, data)))))

    def fixCharacter(self, character):
        """ Fixes the switchingCharacter's data so that the character's model
        and values fit """
        characterName = self.readCharacterName(character)
        switchingCharacterName = self.readSwitchingCharacterName(character)
        switchingCharacter = self.getCharacter(switchingCharacterName)

        if self.disableModelSwitch:
            character = switchingCharacter

        newLevel = self.readCharacterLevel(switchingCharacterName)
        newPromotionLevel = self.readCharacterPromotionLevel(switchingCharacterName)

        if self.forceClassSpread:
            if switchingCharacterName in self.randomizedClasses.keys():
                newClass = self.randomizedClasses[switchingCharacterName]  # take the class of the switching character
                if newPromotionLevel > 0 or (switchingCharacterName in ['Jakob', 'Felicia']):
                    self.setCharacterClass(character, newClass)
                else:
                    if switchingCharacterName == 'Sakura' and self.forceStaffSister and self.gameRoute != 'Conquest':
                        if newClass in ['Onmyoji', 'Priestess']:
                            self.setCharacterClass(character, 'Shrine Maiden')
                        else:
                            self.setCharacterClass(character, 'Troubadour')
                    elif switchingCharacterName == 'Elise' and self.forceStaffSister and self.gameRoute == 'Conquest':
                        if newClass in ['Onmyoji', 'Priestess']:
                            self.setCharacterClass(character, 'Shrine Maiden')
                        else:
                            self.setCharacterClass(character, 'Troubadour')
                    self.setCharacterClass(character, self.readBaseClass(newClass, characterName))

        else:

            # Staff Sister Check
            if switchingCharacterName == 'Sakura' and self.forceStaffSister and self.gameRoute != 'Conquest':
                staffClassSet = self.SISTER_CLASS
                staffClass = self.rng.choice(staffClassSet)
                if staffClass in ['Onmyoji', 'Priestess']:
                    self.setCharacterClass(character, 'Shrine Maiden')
                else:
                    self.setCharacterClass(character, 'Troubadour')
            if switchingCharacterName == 'Elise' and self.forceStaffSister and self.gameRoute == 'Conquest':
                staffClassSet = self.SISTER_CLASS
                staffClass = self.rng.choice(staffClassSet)
                if staffClass in ['Onmyoji', 'Priestess']:
                    self.setCharacterClass(character, 'Shrine Maiden')
                else:
                    self.setCharacterClass(character, 'Troubadour')

            # Staff Retainer Check
            if switchingCharacterName in ['Jakob', 'Felicia'] and self.forceStaffRetainer:
                staffClassSet = self.JAKOB_CLASSES
                if switchingCharacterName == 'Felicia':
                    staffClassSet = self.FELICIA_CLASSES
                staffClass = self.rng.choice(staffClassSet)
                self.setCharacterClass(character, staffClass)

            # Songstress Check
            if switchingCharacterName == 'Azura' and self.forceSongstress:
                self.setCharacterClass(character, 'Songstress')

        # Villager Check
        if switchingCharacterName == 'Mozu' and self.forceVillager:
            self.setCharacterClass(character, 'Villager')

        newClass = self.readClassName(character)
        newBaseClass = self.readBaseClass(newClass, characterName)
        newClassGrowths = self.readClassGrowths(newClass)
        newBaseClassGrowths = self.readClassGrowths(newBaseClass)
        characterData = self.readCharacterData(characterName)
        # ['Stats', 'Growths', 'Modifiers', 'BaseStats', 'Level', 'Name', 'BaseStatsTotal', 'GrowthsTotal', 'PromotionLevel', 'OriginalClass', 'BaseClass']
        characterData['SwitchingCharacterName'] = switchingCharacterName
        characterData['NewBaseClass'] = newBaseClass
        characterData['NewClass'] = newClass
        characterData['NewLevel'] = newLevel
        characterData['NewPromotionLevel'] = newPromotionLevel
        characterData['NewClassGrowths'] = newClassGrowths
        characterData['NewBaseClassGrowths'] = newBaseClassGrowths
        characterData['OldBaseStats'] = characterData['BaseStats']
        characterData['OldGrowths'] = characterData['Growths']

        # # Fix Bitflags
        # bitflags = self.readCharacterBitflags(character)
        # bitflags[1:] = np.zeros(7)
        # bitflags[5] = 64  # MyCastle shops
        # if newClass in self.DRAGON_CLASSES:
        #     bitflags[2] -= 128
        # if newClass in self.BEAST_CLASSES:
        #     bitflags[3] += 1
        # if switchingCharacterName in self.ROYALS:
        #     bitflags[4] += 8
        # if switchingCharacterName == 'Takumi':
        #     bitflags[3] += 64
        # elif switchingCharacterName == 'Ryoma':
        #     bitflags[3] -= 128
        # elif switchingCharacterName == 'Leo':
        #     bitflags[4] += 1
        # elif switchingCharacterName == 'Xander':
        #     bitflags[4] += 2
        # elif switchingCharacterName == 'Ophelia':
        #     bitflags[6] += 1
        # self.setCharacterBitflags(switchingCharacter, bitflags)  # --- DOESN'T WORK
        # self.setCharacterBitflags(character, bitflags)  # --- DOESN'T WORK

        # Adjust Base Stats and Growths
        self.adjustBaseStatsAndGrowths(characterData)

        # Add Variance to Data
        self.addVarianceToData(characterData['Stats'], characterData['Growths'], characterData['Modifiers'])

        # Swap Stats
        self.swapCharacterLck(characterData)
        self.swapCharacterDefRes(characterData)
        self.swapCharacterSklSpd(characterData)
        self.swapCharacterStrMag(characterData)

        # Scale Stats to New Level
        characterBaseStats = characterData['BaseStats']
        characterGrowths = characterData['Growths']
        if characterName == 'Mozu' and self.forceMozuAptitude:
            characterGrowths = np.copy(characterGrowths) + 10
        plusStats = np.zeros(8)
        if newLevel > 1:
            plusStats += (characterGrowths + newClassGrowths) * (newLevel - 1)
        if newPromotionLevel > 1:
            plusStats += (characterGrowths + newBaseClassGrowths) * (newPromotionLevel - 1)
        plusStats = np.floor(plusStats/100)
        characterNewStats = characterBaseStats + plusStats
        characterData['OldStats'] = characterData['Stats']
        characterData['Stats'] = characterNewStats

        if self.verbose:
            print("switchingCharacterName: {}".format(switchingCharacterName))
            print("newLevel, newPromotionLevel: {}, {}".format(newLevel, newPromotionLevel))
            print("OldStats: {}".format(characterData['OldStats']))
            print("OldBaseStats: {}".format(characterData['OldBaseStats']))
            print("OldGrowths: {}".format(characterData['OldGrowths']))
            print("Growths: {}".format(characterData['Growths']))
            print("plusStats: {}".format(plusStats))
            print("BaseStats: {}".format(characterData['BaseStats']))
            print("Stats: {}".format(characterData['Stats']))

        if self.verbose:
            print("--- Update ---")
            print("Growths: {}".format(characterData['Growths']))
            print("Stats: {}".format(characterData['Stats']))

        # Increase Modifiers
        self.increaseModifiers(characterData['Modifiers'])

        # Set Data
        self.setCharacterStats(switchingCharacter, characterData['Stats'])
        self.setCharacterGrowths(switchingCharacter, characterData['Growths'])
        self.setCharacterModifiers(switchingCharacter, characterData['Modifiers'])

        # Randomize Skills
        self.randomizeSkills(switchingCharacter, characterName)

        return switchingCharacter

    def getCharacter(self, characterName):
        """ Returns a reference to the character in the dictionary """
        for character in self.settings['root']['Character']:
            if character['StringData']['@name'] == characterName:
                return character
        raise ValueError('Character named "{}" not found'.format(characterName))

    def increaseModifiers(self, mods):
        """ Increases modifiers """
        for i in range(len(mods)):
            mods[i] += self.modifierCoefficient
        return mods

    def randomizeAllClasses(self):
        self.randomizedClasses = {}
        if len(self.corrinClass) > 0:
            self.randomizedClasses['Corrin'] = self.corrinClass
        else:
            if self.forceSwordCorrin:
                corrinClass = self.rng.choice(self.SWORD_CLASSES)
            else:
                corrinClass = self.rng.choice(self.FINAL_CLASSES)
                while corrinClass == 'Songstress':
                    corrinClass = self.rng.choice(self.FINAL_CLASSES)
                if self.forceStrCorrin:
                    while corrinClass in self.MAGICAL_CLASSES or corrinClass == 'Songstress':
                        corrinClass = self.rng.choice(self.FINAL_CLASSES)
            self.randomizedClasses['Corrin'] = corrinClass

        if self.gameRoute == 'Birthright':
            characters = self.BIRTHRIGHT_CHARACTERS.copy()
        elif self.gameRoute == 'Conquest':
            characters = self.CONQUEST_CHARACTERS.copy()
        elif self.gameRoute == 'Revelations':
            characters = self.REVELATION_CHARACTERS.copy()
        else:
            raise ValueError('gameRoute "{]" unknown'.format(self.gameRoute))

        classes = self.FINAL_CLASSES.copy()
        classes.pop(classes.index(self.randomizedClasses['Corrin']))
        classesBis = self.FINAL_CLASSES.copy()
        classesBis.pop(classesBis.index('Songstress'))  # one Songstress max
        classes = classes + classesBis
        classes = classes[:max(len(classesBis), len(characters))]

        # Staff Sister Check
        if self.forceStaffSister:
            sisterClass = self.rng.choice(self.SISTER_CLASS)
            if self.gameRoute == 'Conquest':
                self.randomizedClasses['Elise'] = sisterClass
                characters.pop(characters.index('Elise'))
                classes.pop(classes.index(sisterClass))
            else:
                self.randomizedClasses['Sakura'] = sisterClass
                characters.pop(characters.index('Sakura'))
                classes.pop(classes.index(sisterClass))

        # Staff Retainer Check
        if self.forceStaffRetainer:
            jakobClass = self.rng.choice(self.JAKOB_CLASSES)
            if self.forceStaffSister:
                while jakobClass == sisterClass:
                    jakobClass = self.rng.choice(self.JAKOB_CLASSES)
            feliciaClass = self.rng.choice(self.FELICIA_CLASSES)
            if self.forceStaffSister:
                while feliciaClass == sisterClass or feliciaClass == jakobClass:
                    feliciaClass = self.rng.choice(self.FELICIA_CLASSES)
            self.randomizedClasses['Jakob'] = jakobClass
            self.randomizedClasses['Felicia'] = feliciaClass
            characters.pop(characters.index('Jakob'))
            characters.pop(characters.index('Felicia'))
            classes.pop(classes.index(jakobClass))
            classes.pop(classes.index(feliciaClass))

        # Songstress Check
        if self.forceSongstress:
            self.randomizedClasses['Azura'] = 'Songstress'
            characters.pop(characters.index('Azura'))
            classes.pop(classes.index('Songstress'))

        # Villager Check
        if self.forceVillager:
            villagerPromoted = self.rng.choice(['Master of Arms', 'Merchant'])
            self.randomizedClasses['Mozu'] = villagerPromoted
            characters.pop(characters.index('Mozu'))
            classes.pop(classes.index(villagerPromoted))

        # prioritize variance in parent classes
        if self.banChildren:
            self.rng.shuffle(classes)
            classes = classes[:len(characters)]
            self.checkGender(characters, classes)
        else:
            childrenStart = characters.index('Shigure')
            parentCharacters = characters[:childrenStart]
            childrenCharacters = characters[childrenStart:]
            parentClasses = classes[:childrenStart]
            childrenClasses = classes[childrenStart:]
            self.rng.shuffle(parentClasses)  # in place
            self.rng.shuffle(childrenClasses)  # in place
            self.checkGender(parentCharacters, parentClasses)
            self.checkGender(childrenCharacters, childrenClasses)
            classes = parentClasses + childrenClasses

        for i, className in enumerate(classes):
            self.randomizedClasses[characters[i]] = className

        return None

    def randomizeSkills(self, switchingCharacter, characterName):
        switchingCharacterName = self.readCharacterName(switchingCharacter)
        nSkills = self.nSkills
        if self.nSkills == -1:
            skills = self.readSkills(switchingCharacter)
            nSkills = len(np.nonzero(skills)[0])
        skills = self.sampleSkills(nSkills)
        if characterName == 'Mozu':
            if self.forceMozuAptitude:
                if 108 not in skills:
                    skills[-1] = 108
        if switchingCharacterName == 'Mozu':
            if self.forceVillager:
                if 108 not in skills:
                    skills[-1] = 108
        if switchingCharacterName == 'Kaze':
            if self.forceLocktouch:
                if 112 not in skills:
                    skills[-1] = 112
        return self.setCharacterSkills(switchingCharacter, skills)

    def readBaseClass(self, className, characterName):
        """ Returns a possible base class for a promoted class
            or the same class for an unpromoted one """
        baseClasses = self.classData[className]['BaseClasses']
        if className in ['Nohr Noble', 'Hoshido Noble']:
            if characterName in self.MALE_CHARACTERS:
                return 'Nohr Prince'
            else:
                return 'Nohr Princess'
        elif className == 'Onmyoji':
            baseClass = self.rng.choice(['Diviner', 'Monk'])
            if baseClass == 'Monk' and characterName in self.FEMALE_CHARACTERS:
                return 'Shrine Maiden'
            else:
                return baseClass
        elif len(baseClasses) == 0:
            return className
        else:
            return self.rng.choice(baseClasses)

    def readCharacterBaseClass(self, characterName):
        return self.allCharacterData[characterName]['BaseClass']

    def readCharacterBaseStats(self, characterName):
        return np.copy(self.allCharacterData[characterName]['BaseStats'])

    def readCharacterBitflags(self, character):
        bitflags = character['Bitflags']['@values']
        return np.array(list(map(int, bitflags.split(','))))

    def readCharacterData(self, characterName):
        return self.allCharacterData[characterName].copy()

    def readCharacterGrowths(self, characterName):
        return np.copy(self.allCharacterData[characterName]['Growths'])

    def readCharacterModifiers(self, characterName):
        return np.copy(self.allCharacterData[characterName]['Modifiers'])

    def readCharacterName(self, character):
        return character['StringData']['@name']

    def readCharacterLevel(self, characterName):
        return self.allCharacterData[characterName]['Level']

    def readCharacterOriginalClass(self, characterName):
        return self.allCharacterData[characterName]['OriginalClass']

    def readCharacterPromotionLevel(self, characterName):
        return self.allCharacterData[characterName]['PromotionLevel']

    def readCharacterStats(self, characterName):
        return np.copy(self.allCharacterData[characterName]['Stats'])

    def readClassAttackType(self, className):
        return self.classData[className]['AttackType']

    def readClassGrowths(self, className):
        return np.copy(self.classData[className]['Growths'])

    def readClassName(self, character):
        return character['ClassData']['@class']

    def readSkills(self, character):
        skills = character['Skills']['@values']
        return np.array(list(map(int, skills.split(','))))

    def readSwitchedCharacterName(self, characterName):
        """ Returns a reference to the switched character in the dictionary """
        if characterName == 'Corrin':
            return 'Corrin'
        for character in self.settings['root']['Character']:
            if character['StringData']['@switchingCharacter'] == characterName:
                return character['StringData']['@name']
        raise ValueError('Character named "{}" not found'.format(characterName))

    def readSwitchingCharacterName(self, character):
        return character['StringData']['@switchingCharacter']

    def sampleSkills(self, nSkills):
        """ Player-available skills: 1->112, 120->122, 128->159
        (147 skills total)
        Excludes Aptitude (108), Bold Stance (120), Point Blank (121), Winged Shield (122),
        Paragon (138), Armor Shield (139), Beast Shield (140), Taker Skills (142->148),
        Ballistician skills (149->152), Warp (154).
        Remaining Skills: 1->107, 109->112, 128->137, 141, 153, 155->159 (128 skills) """
        skills = self.rng.choice(128, 5, replace=False) + 1
        for i, s in enumerate(skills):
            if s >= 124:
                skills[i] = s + 31
            elif s == 123:
                skills[i] = 153
            elif s == 122:
                skills[i] = 141
            elif s >= 112:
                skills[i] = s + 16
            elif s >= 108:
                skills[i] = s + 1
            elif s == 0:
                skills[i] = 159
        for i in range(nSkills, 5):  # erase added skills if needed
            skills[i] = 0
        return skills

    def setCharacterBitflags(self, character, bitflags):
        character['Bitflags']['@values'] = self.dataToString(bitflags)
        return character

    def setCharacterClass(self, character, className):
        character['ClassData']['@class'] = className
        return character

    def setCharacterGrowths(self, character, growths):
        character['Growths']['@values'] = self.dataToString(growths)
        return character

    def setCharacterModifiers(self, character, modifiers):
        character['Modifiers']['@values'] = self.dataToString(modifiers)
        return character

    def setCharacterStats(self, character, stats):
        character['Stats']['@values'] = self.dataToString(stats)
        return character

    def setCharacterSkills(self, character, skills):
        character['Skills']['@values'] = self.dataToString(skills)
        return character

    def swapCharacterDefRes(self, characterData):
        if characterData['SwitchingCharacterName'] == 'Gunter' and self.forceGunterDef:
            i, j = 6, 7
            growths = characterData['Growths']
            if growths[i] < growths[j]:
                growths[i], growths[j] = growths[j], growths[i]

            stats = characterData['Stats']
            if stats[i] < stats[j]:
                stats[i], stats[j] = stats[j], stats[i]

            modifiers = characterData['Modifiers']
            if modifiers[i] < modifiers[j]:
                modifiers[i], modifiers[j] = modifiers[j], modifiers[i]

        elif self.rng.random() < self.swapDefResP:
            growths = characterData['Growths']
            growths[6], growths[7] = growths[7], growths[6]

            stats = characterData['Stats']
            stats[6], stats[7] = stats[7], stats[6]

            modifiers = characterData['Modifiers']
            modifiers[6], modifiers[7] = modifiers[7], modifiers[6]

        return characterData

    def swapCharacterLck(self, characterData):
        if self.swapLckP < 0 or self.swapLckP > 1:
            s = self.rng.choice(7)
            if s == 5:  # Lck mapped to Res
                s = 7
            growths = characterData['Growths']
            threshold = growths[5]/100  # Lck Growth

            if self.rng.random() < threshold and growths[5] > growths[s]:
                growths[5], growths[s] = growths[s], growths[5]

            stats = characterData['Stats']
            if self.rng.random() < threshold and stats[5] > stats[s]:
                stats[5], stats[s] = stats[s], stats[5]

            modifiers = characterData['Modifiers']
            if self.rng.random() < threshold and modifiers[5] > modifiers[s]:
                modifiers[5], modifiers[s] = modifiers[s], modifiers[5]

        elif self.rng.random() < self.swapLckP:
            growths = characterData['Growths']
            growths[5], growths[s] = growths[s], growths[5]

            stats = characterData['Stats']
            stats[5], stats[s] = stats[s], stats[5]

            modifiers = characterData['Modifiers']
            modifiers[5], modifiers[s] = modifiers[s], modifiers[5]

            return characterData

    def swapCharacterSklSpd(self, characterData):
        if self.rng.random() < self.swapSklSpdP:
            growths = characterData['Growths']
            growths[3], growths[4] = growths[4], growths[3]

            stats = characterData['Stats']
            stats[3], stats[4] = stats[4], stats[3]

            modifiers = characterData['Modifiers']
            modifiers[3], modifiers[4] = modifiers[4], modifiers[3]

        return characterData

    def swapCharacterStrMag(self, characterData):
        if self.swapStrMagP < 0 or self.swapStrMagP > 1:
            className = characterData['NewClass']
            classAttackType = self.readClassAttackType(className)
            i, j = 1, 2  # default: 'Str'
            if classAttackType == 'Mag':
                i, j = 2, 1
            elif classAttackType == 'Mixed':
                if self.rng.random() < 0.5:
                    i, j = 2, 1

            growths = characterData['Growths']
            if growths[i] < growths[j]:
                growths[i], growths[j] = growths[j], growths[i]

            stats = characterData['Stats']
            if stats[i] < stats[j]:
                stats[i], stats[j] = stats[j], stats[i]

            modifiers = characterData['Modifiers']
            if modifiers[i] < modifiers[j]:
                modifiers[i], modifiers[j] = modifiers[j], modifiers[i]

        elif self.rng.random() < self.swapStrMagP:
            growths = characterData['Growths']
            growths[1], growths[2] = growths[2], growths[1]

            stats = characterData['Stats']
            stats[1], stats[2] = stats[2], stats[1]

            modifiers = characterData['Modifiers']
            modifiers[1], modifiers[2] = modifiers[2], modifiers[1]

            return characterData

    def run(self):
        if self.forceClassSpread:
            with open('{}/ClassSpread.csv'.format(path), 'w') as fcsv:
                writer = csv.writer(fcsv, delimiter='\t')
                for name in self.randomizedClasses.keys():
                    className = self.randomizedClasses[name]
                    row = [name, self.readSwitchedCharacterName(name), className]
                    writer.writerow(row)

        for character in self.settings['root']['Character']:
            self.fixCharacter(character)

        with open('{}/RandomizerSettingsUpdated.xml'.format(path), 'w') as fxml:
            fxml.write(xmltodict.unparse(self.settings, pretty=True))


## Run the randomizer

if __name__ == "__main__":
    fatesRandomizer = FatesRandomizer(
        allCharacterData,
        classData,
        settings,
        addmaxPow=args.addmax_pow,
        banAmiiboCharacters=args.ban_amiibo_characters,
        banAnna=args.ban_anna,
        banBallistician=(not args.allow_ballistician),
        banChildren=args.ban_children,
        banDLCClasses=args.ban_dlc_classes,
        banWitch=args.ban_witch,
        baseStatsSumMax=args.base_stats_sum,
        corrinClass=args.corrin_class,
        disableModelSwitch=args.disable_model_switch,
        forceClassSpread=(not args.disable_class_spread),
        forceGunterDef=(not args.disable_gunter_def),
        forceLocktouch=(not args.disable_locktouch),
        forceMozuAptitude=(args.enforce_mozu_aptitude),
        forceStaffRetainer=(not args.disable_staff_retainer),
        forceStaffSister=(not args.disable_staff_sister),
        forceStatDecrease=args.enforce_stat_decrease,
        forceStatIncrease=args.enforce_stat_increase,
        forceSongstress=(not args.disable_songstress),
        forceStrCorrin=(not args.enable_mag_only_corrin),
        forceSwordCorrin=args.enforce_sword_corrin,
        forceVillager=args.enforce_villager,
        gameRoute=args.game_route,
        growthCap=args.growth_cap,
        growthP=args.growth_p,
        growthsSumMin=args.growths_sum_min,
        modifierCoefficient=args.modifier_coefficient,
        modP=args.mod_p,
        nPasses=args.n_passes,
        nSkills=args.n_skills,
        seed=args.seed,
        statP=args.stat_p,
        swapDefResP=args.swap_def_res_p,
        swapLckP=args.swap_lck_p,
        swapSklSpdP=args.swap_skl_spd_p,
        swapStrMagP=args.swap_str_mag_p,
        verbose=args.verbose
    )

    fatesRandomizer.run()
