# -*- coding: utf-8 -*-

import xmltodict
import csv
import numpy as np
import argparse
from numpy.random import default_rng


## Initialize path and arguments

path = './data'

parser = argparse.ArgumentParser()
parser.add_argument('-ap', '--addmax-pow', type=float, default=0.8, help="the lower the more uniform growth adjustment")
parser.add_argument('-ab', '--allow-ballistician', action='store_true', help="allow Ballistician class in the randomization")
parser.add_argument('-ads', '--allow-dlc-skills', action='store_true', help="allow DLC skills in skill randomization")
parser.add_argument('-ba', '--ban-anna', action='store_true', help="ban Anna")
parser.add_argument('-bac', '--ban-amiibo-characters', action='store_true', help="ban Amiibo characters (Marth, Lucina, Robin, Ike)")
parser.add_argument('-bc', '--ban-children', action='store_true', help="ban children characters")
parser.add_argument('-bdc', '--ban-dlc-classes', action='store_true', help="ban DLC classes")
parser.add_argument('-bdcs', '--ban-dlc-class-skills', action='store_true', help="ban DLC class skills in skill randomization")
parser.add_argument('-bscap', '--base-stat-cap', type=int, default=11, help="if adjusting growths, max value for base stat")
parser.add_argument('-bssmax', '--base-stats-sum-max', type=int, default=30, help="if adjusting growths, decreasing stats sum to that value")
parser.add_argument('-bssmin', '--base-stats-sum-min', type=int, default=15, help="if adjusting growths, increasing stats sum to that value")
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
parser.add_argument('-dbsr', '--disable-balanced-skill-randomization', action='store_true', help="disable balanced skill randomization; skill randomization will be completely random")
parser.add_argument('-dcd', '--disable-camilla-def', action='store_true', help="disable Camilla's replacement's enforced higher Def than Res")
parser.add_argument('-dcs', '--disable-class-spread', action='store_true', help="disable diverse class reroll")
parser.add_argument('-dgd', '--disable-gunter-def', action='store_true', help="disable Gunter's replacement's enforced higher Def than Res")
parser.add_argument('-dlts', '--disable-livetoserve', action='store_true', help="disable the retainers' replacements' enforced Live to Serve skill")
parser.add_argument('-dl', '--disable-locktouch', action='store_true', help="disable Kaze and Niles' replacements' enforced Locktouch skill")
parser.add_argument('-dms', '--disable-model-switch', action='store_true', help="disable model switching but keep switching the rest of the data (stats, growths...)")
parser.add_argument('-drl', '--disable-rebalance-levels', action='store_true', help="disable fairer level balance adjustments (reverts to levels from the original games)")
parser.add_argument('-drsgs', '--disable-randomize-stats-growths-sum', action='store_true', help="will disable randomizing stats and growths sum for each character between customizable bounds")
parser.add_argument('-ds', '--disable-songstress', action='store_true', help="disable Azura's replacement's enforced Songstress class")
parser.add_argument('-dsr', '--disable-staff-retainer', action='store_true', help="disable Jakob and Felicia's replacement's enforced healing class")
parser.add_argument('-dss', '--disable-staff-early-recruit', action='store_true', help="disable Sakura and/or Elise's replacement's enforced healing class")
parser.add_argument('-edbc', '--enable-dlc-base-class', action='store_true', help="will give unpromoted base classes to every DLC class for game balance (eg Ninja/Oni Savage for Dread Fighter)")
parser.add_argument('-egd', '--enable-genderless-dlc', action='store_true', help="allows DLC classes to be given regardless of gender; can cause the randomizer to fail if a prepromoted character gets a gender-locked DLC class")
parser.add_argument('-elsc', '--enable-limit-staff-classes', action='store_true', help="will replace staff only class by a magical class and set the staff only class as a reclass option")
parser.add_argument('-ema', '--enforce-mozu-aptitude', action='store_true', help="enforce Mozu (herself) having Aptitude")
parser.add_argument('-emoc', '--enable-mag-only-corrin', action='store_true', help="enables Corrin to get a Mag only class")
parser.add_argument('-epa', '--enforce-paralogue-aptitude', action='store_true', help="enforce Mozu's replacement to have Aptitude")
parser.add_argument('-esc', '--enforce-sword-corrin', action='store_true', help="enforces Corrin to get a sword-wielding final class")
parser.add_argument('-esd', '--enforce-stat-decrease', action='store_true', help="enforces stat decrease to base stat sum max regardless of growth increase")
parser.add_argument('-esi', '--enforce-stat-increase', action='store_true', help="enforces stat increase to base stat sum min")
parser.add_argument('-ev', '--enforce-villager', action='store_true', help="enforce Mozu's replacement being a Villager with Aptitude")
parser.add_argument('-evc', '--enforce-viable-characters', action='store_true', help="will force you to play with only the first 15 characters encoutered by giving 0 growth rates to the others in the route; non-iable characters will be given the 'Survey' skill for easy identification")
parser.add_argument('-g', '--game-route', choices=['Revelations', 'Birthright', 'Conquest'], default='', help="game route, especially important to specify it if playing Revelations so that levels are the correct ones")
parser.add_argument('-gc', '--growth-cap', type=int, default=70, help="adjusted growths cap")
parser.add_argument('-gp', '--growth-p', type=float, default=1., help="probability of editing growths in a variability pass")
parser.add_argument('-gsmax', '--growths-sum-max', type=int, default=350, help="will adjust growths until sum is lower than specified value")
parser.add_argument('-gsmin', '--growths-sum-min', type=int, default=250, help="will adjust growths until sum is higher than specified value")
parser.add_argument('-mc', '--modifier-coefficient', type=int, default=0, help="will increase all modifiers by specified coefficient")
parser.add_argument('-mp', '--mod-p', type=float, default=0.25, help="probability of editing modifiers in a variability pass")
parser.add_argument('-np', '--n-passes', type=int, default=10, help="number of variability passes (swap +/- 5 growths, +/- 1 stats and mods per pass")
parser.add_argument('-ns', '--n-skills', type=int, default=-1, choices=[-1, 0, 1, 2, 3, 4, 5], help="number of randomized skills; if -1, randomize existing skills")
parser.add_argument('-pmu', '--pmu-mode', action='store_true', help="`ClassSpread.csv` will only contain the 16 allowed characters for the run")
parser.add_argument('-s', '--seed', type=int, default=None, help="RNG seed")
parser.add_argument('-sp', '--stat-p', type=float, default=0.5, help="probability of editing stats in a variability pass")
parser.add_argument('-sadp', '--swap-atk-def-p', type=float, default=0.2, help="probability of swapping Str/Mag (higher one) with Def/Res (higher one) growths / stats / modifiers")
parser.add_argument('-sdrp', '--swap-def-res-p', type=float, default=0.2, help="probability of swapping Def and Res growths / stats / modifiers")
parser.add_argument('-slp', '--swap-lck-p', type=float, default=-1., help="probability of swapping Lck and a random stat's growths / stats / modifiers; random if between 0 and 1, else [(Lck Growth)%% and swap only if Lck is superior]")
parser.add_argument('-sssp', '--swap-skl-spd-p', type=float, default=0.2, help="probability of swapping Skl and Spd growths / stats / modifiers")
parser.add_argument('-ssmp', '--swap-str-mag-p', type=float, default=0., help="probability of swapping Str and Mag growths / stats / modifiers; random if between 0 and 1, else according to class (coin flip for mixed classes)")
parser.add_argument('-v', '--verbose', action='store_true', help="print verbose stuff")
args = parser.parse_args()


## Load data

with open('{}/fates_data_hub.csv'.format(path)) as fcsv:
    reader = csv.reader(fcsv)
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
        rebalancedLevel = int(row[39])
        revelationsLevel = int(row[40])
        rebalancedRevelationsLevel = int(row[41])
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
            'BaseClass': baseClass,
            'RebalancedLevel': rebalancedLevel,
            'RevelationsLevel': revelationsLevel,
            'RebalancedRevelationsLevel': rebalancedRevelationsLevel
        }


with open('{}/fates_class_data.csv'.format(path)) as fcsv:
    reader = csv.reader(fcsv)
    classData = {}
    next(reader)
    for row in reader:
        baseClasses = row[11:13]
        weapons = row[13:]
        while len(weapons) > 0:
            if weapons[-1] == '':
                weapons.pop()
            else:
                break
        while len(baseClasses) > 0:
            if baseClasses[-1] == '':
                baseClasses.pop()
            else:
                break
        classData[row[0]] = {
            'AttackType': row[1],
            'DefenseType': row[2],
            'Growths': list(map(int, row[3:11])),
            'BaseClasses': baseClasses,
            'Weapons': weapons
        }


with open('{}/RandomizerSettings.xml'.format(path), 'rb') as fxml:
    settings = xmltodict.parse(fxml.read().decode('utf-8'))


## Randomizer Class

class FatesRandomizer:
    def __init__(
        self,
        allCharacterData,
        classData,
        settings,
        addmaxPow=0.8,
        allowDLCSkills=False,
        banAmiiboCharacters=False,
        banAnna=False,
        banBallistician=True,
        banChildren=False,
        banDLCClasses=False,
        banDLCClassSkills=False,
        banWitch=False,
        baseStatCap=11,  # in adjustBaseStatsAndGrowths, max value for base stats
        baseStatsSumMax=30,  # in adjustBaseStatsAndGrowths, if growths have to be increased, will decrease stats sum to said value
        baseStatsSumMin=15,  # in adjustBaseStatsAndGrowths, will increase stats sum to said value
        corrinClass='',
        disableBalancedSkillRandomization=False,
        disableModelSwitch=False,  # will disable model switching
        enableGenderlessDLC=False,  # allows DLC classes to be given regardless of gender
        enableDLCBaseClass=False,  # will give unpromoted base classes to every DLC class for game balance (eg Ninja/Oni Savage for Dread Fighter)
        forceClassSpread=True,  # will limit class duplicates
        forceCamillaDef=True,  # will force Camilla's replacement to have higher Def
        forceGunterDef=True,  # will force Gunter's replacement to have higher Def
        forceLiveToServe=True,  # will force the retainers' replacements to get Live to Serve
        forceLocktouch=True,  # will force Kaze's replacement to get Locktouch
        forceMozuAptitude=False,  # will force Mozu (not her replacement) to get Aptitude
        forceParalogueAptitude=False,  # will force Mozu's replacement to get Aptitude
        forceStaffRetainer=True,  # will force the retainer's replacement to get a promoted class with a staff
        forceStaffEarlyRecruit=True,  # will force an early recruit replacement to get a healing class
        forceStatDecrease=False,  # force stat decrase in adjustBaseStatsAndGrowths
        forceStatIncrease=False,  # force stat increase in adjustBaseStatsAndGrowths
        forceSongstress=True,  # will force Azura's replacement to be a Songstress
        forceStrCorrin=True,  # will force Corrin to have a class that wields at least one Str weapon
        forceSwordCorrin=False,  # will force Corrin to have a class that wields swords
        forceViableCharacters=False,  # will give 0 growths and the Survey skill to all characters except the first 15 encountered
        forceVillager=False,  # will force Mozu's replacement to be a Villager and get Aptitude
        gameRoute='',  # 'Birthright', 'Conquest' or 'Revelations', used in randomizeClasses
        growthCap=70,  # growth cap in adjustBaseStatsAndGrowths
        growthP=1,  # proba of editing growths in AddVariancetoData
        growthsSumMax=350,  # in adjustBaseStatsAndGrowths, will decrease growths sum down to said value
        growthsSumMin=250,  # in adjustBaseStatsAndGrowths, will increase growths sum up to said value
        limitStaffClasses=False,  # will limit staff only classes by putting characters in a magical class and offering the staff class as a possible reclass
        modifierCoefficient=0,  # value by which all modifiers will be increased
        modP=0.25,  # proba of editing modifiers in AddVariancetoData
        nPasses=10,  # number of passes in AddVariancetoData
        nSkills=-1,  # if -1, randomize existing skills
        PMUMode=False,  # ClassSpread.csv will contain only the 16 allowed characters, other characters will have the Survey skill
        randomizeStatsAndGrowthsSum=True,  # will sample a random value between min and max for each character
        rebalanceLevels=True,  # will rebalance recruitment levels
        seed=None,
        statP=0.5,  # proba of editing stats in AddVariancetoData
        swapAtkDefP=0,  # according to class before random
        swapDefResP=0.2,  # according to class before random
        swapLckP=-1, # random if between 0 and 1, else [(Lck Growth)% and only swap if Lck is superior]
        swapSklSpdP=0.2,  # random
        swapStrMagP=0.,  # according to class before random
        verbose=False
    ):
        self.allCharacterData = allCharacterData.copy()
        self.classData = classData.copy()
        self.settings = settings.copy()

        assert nSkills <= 5, "nSkills must be <= 5"

        self.addmaxPow = addmaxPow
        self.allowDLCSkills = allowDLCSkills
        self.banAmiiboCharacters = banAmiiboCharacters
        self.banAnna = banAnna
        self.banChildren = banChildren
        self.banBallistician = banBallistician
        self.banDLCClasses = banDLCClasses
        self.banDLCClassSkills = banDLCClassSkills
        self.banWitch = banWitch
        self.baseStatCap=baseStatCap
        self.baseStatsSumMax = baseStatsSumMax
        self.baseStatsSumMin = baseStatsSumMin
        self.corrinClass = corrinClass
        self.disableBalancedSkillRandomization = disableBalancedSkillRandomization
        self.disableModelSwitch = disableModelSwitch
        self.enableDLCBaseClass = enableDLCBaseClass
        self.enableGenderlessDLC = enableGenderlessDLC
        self.forceClassSpread = forceClassSpread
        self.forceCamillaDef = forceCamillaDef
        self.forceGunterDef = forceGunterDef
        self.forceLiveToServe = forceLiveToServe
        self.forceLocktouch = forceLocktouch
        self.forceMozuAptitude = forceMozuAptitude
        self.forceParalogueAptitude = forceParalogueAptitude
        self.forceStaffRetainer = forceStaffRetainer
        self.forceStaffEarlyRecruit = forceStaffEarlyRecruit
        self.forceStatDecrease = forceStatDecrease
        self.forceStatIncrease = forceStatIncrease
        self.forceSongstress = forceSongstress
        self.forceStrCorrin = forceStrCorrin
        self.forceSwordCorrin = forceSwordCorrin
        self.forceViableCharacters = forceViableCharacters
        self.forceVillager = forceVillager
        self.gameRoute = gameRoute
        self.growthCap = growthCap
        self.growthP = growthP
        self.growthsSumMax = growthsSumMax
        self.growthsSumMin = growthsSumMin
        self.limitStaffClasses = limitStaffClasses
        self.modifierCoefficient = modifierCoefficient
        self.modP = modP
        self.nPasses = nPasses
        self.nSkills = nSkills
        self.PMUMode = PMUMode
        self.randomizeStatsAndGrowthsSum = randomizeStatsAndGrowthsSum
        self.rebalanceLevels = rebalanceLevels
        self.rng = default_rng(seed)
        self.statP = statP
        self.swapAtkDefP = swapAtkDefP
        self.swapDefResP = swapDefResP
        self.swapLckP = swapLckP
        self.swapSklSpdP = swapSklSpdP
        self.swapStrMagP = swapStrMagP
        self.verbose=verbose

        if self.gameRoute == '':
            print("Note: if you are planning to play Revelations, please use the option [-g \"Revelations\"], otherwise recruitment levels will not be correct.")

        self.BEAST_CLASSES = ['Wolfskin', 'Wolfssegner', 'Kitsune', 'Nine-Tails']
        self.DRAGON_CLASSES = ['Nohr Prince', 'Nohr Princess', 'Nohr Noble', 'Hoshido Noble']

        self.FELICIA_CLASSES = ['Hoshido Noble', 'Onmyoji', 'Priestess',
                                'Falcon Knight', 'Adventurer', 'Strategist', 'Maid']
        self.JAKOB_CLASSES = ['Hoshido Noble', 'Onmyoji', 'Great Master',
                              'Falcon Knight', 'Adventurer', 'Strategist', 'Butler']
        self.MALE_STAFF_CLASSES = ['Onmyoji', 'Strategist', 'Butler', 'Great Master']
        self.FEMALE_STAFF_CLASSES = ['Onmyoji', 'Priestess', 'Strategist', 'Maid']

        if self.enableGenderlessDLC:
            self.MALE_CLASSES = ['Great Master', 'Butler']
            self.FEMALE_CLASSES = ['Priestess', 'Maid']
        else:
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
        self.TOME_CLASSES = [
            'Oni Chieftain', 'Basara', 'Onmyoji', 'Nohr Noble',
            'Malig Knight', 'Dark Knight', 'Strategist',
            'Dark Falcon', 'Witch', 'Grandmaster'
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
            'Troubadour', 'Wolfskin'
        ]

        self.AMIIBO_CHARACTERS = ['Marth', 'Lucina', 'Robin', 'Ike']

        self.BIRTHRIGHT_CHARACTERS = [
            'Felicia', 'Jakob', 'Kaze', 'Rinkah', 'Azura', 'Sakura', 'Hana', 'Subaki',
            'Silas', 'Saizo', 'Orochi', 'Mozu', 'Hinoka', 'Azama', 'Setsuna',
            'Hayato', 'Oboro', 'Hinata', 'Takumi', 'Kagero', 'Reina', 'Kaden', 'Ryoma',
            'Scarlet', 'Izana', 'Shura', 'Yukimura', 'Anna', 'Shigure', 'Dwyer', 'Sophie',
            'Midori', 'Shiro', 'Kiragi', 'Asugi', 'Selkie', 'Hisame', 'Mitama', 'Caeldori',
            'Rhajat', 'Marth', 'Lucina', 'Robin', 'Ike', 'Gunter'
        ]
        self.CONQUEST_CHARACTERS = [
            'Felicia', 'Jakob', 'Elise', 'Silas', 'Arthur', 'Effie', 'Mozu',
            'Odin', 'Niles', 'Azura', 'Nyx', 'Camilla', 'Selena', 'Beruka', 'Kaze',
            'Laslow', 'Peri', 'Benny', 'Charlotte', 'Leo', 'Keaton', 'Gunter',
            'Xander', 'Shura', 'Flora', 'Izana', 'Anna', 'Shigure', 'Dwyer', 'Sophie',
            'Midori', 'Siegbert', 'Forrest', 'Ignatius', 'Velouria', 'Percy',
            'Ophelia', 'Soleil', 'Nina', 'Marth', 'Lucina', 'Robin', 'Ike',
        ]
        self.REVELATION_CHARACTERS = [
            'Azura', 'Felicia', 'Jakob', 'Mozu', 'Sakura', 'Hana',
            'Subaki', 'Kaze', 'Rinkah', 'Takumi', 'Oboro', 'Hinata',
            'Saizo', 'Orochi', 'Reina', 'Kagero', 'Camilla', 'Selena', 'Beruka',
            'Kaden', 'Keaton', 'Elise', 'Arthur', 'Effie', 'Charlotte', 'Benny',
            'Silas', 'Shura', 'Nyx', 'Hinoka', 'Azama', 'Setsuna', 'Ryoma',
            'Scarlet', 'Leo', 'Xander', 'Odin', 'Niles', 'Laslow', 'Peri',
            'Flora', 'Fuga', 'Anna', 'Shigure', 'Dwyer', 'Sophie', 'Midori', 'Shiro',
            'Kiragi', 'Asugi', 'Selkie', 'Hisame', 'Mitama', 'Caeldori', 'Rhajat',
            'Siegbert', 'Forrest', 'Ignatius', 'Velouria', 'Percy', 'Ophelia',
            'Soleil', 'Nina', 'Marth', 'Lucina', 'Robin', 'Ike', 'Gunter',
        ]  # removed Hayato
        self.ALL_CHARACTERS = [
            'Azura', 'Felicia', 'Jakob', 'Mozu', 'Sakura', 'Hana', 'Subaki',
            'Kaze', 'Rinkah', 'Hayato', 'Takumi', 'Oboro', 'Hinata', 'Saizo',
            'Orochi', 'Reina', 'Kagero', 'Camilla', 'Selena', 'Beruka', 'Kaden',
            'Keaton', 'Elise', 'Arthur', 'Effie', 'Charlotte', 'Benny', 'Silas',
            'Shura', 'Nyx', 'Hinoka', 'Azama', 'Setsuna', 'Ryoma', 'Scarlet', 'Leo',
            'Xander', 'Odin', 'Niles', 'Laslow', 'Peri', 'Flora', 'Fuga', 'Anna',
            'Izana', 'Yukimura', 'Gunter', 'Shigure', 'Dwyer', 'Sophie', 'Midori', 'Shiro',
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
        self.FAIRE_SKILLS = {
            "Sword": 65,
            "Lance": 66,
            "Axe": 67,
            "Dagger": 68,
            "Bow": 69,
            "Tome": 70,
        }
        self.BREAKER_SKILLS = {
            "Sword": 81,
            "Lance": 79,
            "Axe": 80,
            "Dagger": 84,
            "Bow": 82,
            "Tome": 83,
        }

        # if self.gameRoute == "Birthright":
        #     self.allowedCharacters = [
        #     'Felicia', 'Jakob', 'Kaze', 'Rinkah', 'Azura', 'Sakura', 'Hana', 'Subaki',
        #     'Silas', 'Saizo', 'Orochi', 'Mozu', 'Hinoka', 'Azama', 'Setsuna', 'Oboro'
        # ]
        # elif self.gameRoute == "Conquest":
        #     self.allowedCharacters = [
        #     'Felicia', 'Jakob', 'Elise', 'Silas', 'Arthur', 'Effie', 'Mozu', 'Odin',
        #     'Niles', 'Azura', 'Nyx', 'Camilla', 'Selena', 'Benny', 'Kaze', 'Laslow',
        # ]
        # else:
        #     self.allowedCharacters = [
        #     'Azura', 'Felicia', 'Jakob', 'Mozu', 'Sakura', 'Hana',
        #     'Subaki', 'Kaze', 'Rinkah', 'Hayato', 'Takumi', 'Oboro', 'Hinata',
        #     'Saizo', 'Orochi', 'Kaden'
        # ]

        if self.enableDLCBaseClass:
            self.PROMOTED_CLASSES += self.DLC_CLASSES
        else:
            self.UNPROMOTED_CLASSES += self.DLC_CLASSES
            for className in self.DLC_CLASSES:
                self.classData[className]['BaseClasses'] = []

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
                self.ALL_CHARACTERS.pop(self.ALL_CHARACTERS.index(characterName))
        if self.banAnna:
            self.FEMALE_CHARACTERS.pop(self.FEMALE_CHARACTERS.index('Anna'))
            self.BIRTHRIGHT_CHARACTERS.pop(self.BIRTHRIGHT_CHARACTERS.index('Anna'))
            self.CONQUEST_CHARACTERS.pop(self.CONQUEST_CHARACTERS.index('Anna'))
            self.REVELATION_CHARACTERS.pop(self.REVELATION_CHARACTERS.index('Anna'))
            self.ALL_CHARACTERS.pop(self.ALL_CHARACTERS.index('Anna'))
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
                self.ALL_CHARACTERS.pop(self.ALL_CHARACTERS.index(characterName))

        if self.banDLCClasses:
            for className in self.DLC_CLASSES:
                if className in self.MALE_CLASSES:
                    self.MALE_CLASSES.pop(self.MALE_CLASSES.index(className))
                if className in self.FEMALE_CLASSES:
                    self.FEMALE_CLASSES.pop(self.FEMALE_CLASSES.index(className))
                if className in self.FINAL_CLASSES:
                    self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index(className))
                if className in self.PROMOTED_CLASSES:
                    self.PROMOTED_CLASSES.pop(self.PROMOTED_CLASSES.index(className))
                if className in self.UNPROMOTED_CLASSES:
                    self.UNPROMOTED_CLASSES.pop(self.UNPROMOTED_CLASSES.index(className))
                if className in self.MAGICAL_CLASSES:
                    self.MAGICAL_CLASSES.pop(self.MAGICAL_CLASSES.index(className))
                if className in self.SWORD_CLASSES:
                    self.SWORD_CLASSES.pop(self.SWORD_CLASSES.index(className))
        else:
            if self.banBallistician:
                if 'Ballicistian' in self.MALE_CLASSES:
                    self.MALE_CLASSES.pop(self.MALE_CLASSES.index('Ballistician'))
                self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index('Ballistician'))
                if 'Ballicistian' in self.UNPROMOTED_CLASSES:
                    self.UNPROMOTED_CLASSES.pop(self.UNPROMOTED_CLASSES.index('Ballistician'))
                elif 'Ballicistian' in self.PROMOTED_CLASSES:
                    self.PROMOTED_CLASSES.pop(self.PROMOTED_CLASSES.index('Ballistician'))
            if self.banWitch:
                if 'Witch' in self.FEMALE_CLASSES:
                    self.FEMALE_CLASSES.pop(self.FEMALE_CLASSES.index('Witch'))
                self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index('Witch'))
                if 'Witch' in self.UNPROMOTED_CLASSES:
                    self.UNPROMOTED_CLASSES.pop(self.UNPROMOTED_CLASSES.index('Witch'))
                elif 'Witch' in self.PROMOTED_CLASSES:
                    self.PROMOTED_CLASSES.pop(self.PROMOTED_CLASSES.index('Witch'))
                self.MAGICAL_CLASSES.pop(self.MAGICAL_CLASSES.index('Witch'))

        # Wrong noble classes disable supports with prepromoted units
        if self.gameRoute not in ['Conquest', 'Revelations']:
            self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index('Nohr Noble'))
            self.PROMOTED_CLASSES.pop(self.PROMOTED_CLASSES.index('Nohr Noble'))
            self.SWORD_CLASSES.pop(self.SWORD_CLASSES.index('Nohr Noble'))
        elif self.gameRoute != 'Birthright':  # Revelations doesn't like the 'Hoshido Noble' class apparently
            self.JAKOB_CLASSES.pop(self.JAKOB_CLASSES.index('Hoshido Noble'))
            self.FELICIA_CLASSES.pop(self.FELICIA_CLASSES.index('Hoshido Noble'))
            self.FINAL_CLASSES.pop(self.FINAL_CLASSES.index('Hoshido Noble'))
            self.PROMOTED_CLASSES.pop(self.PROMOTED_CLASSES.index('Hoshido Noble'))
            self.SWORD_CLASSES.pop(self.SWORD_CLASSES.index('Hoshido Noble'))

        self.earlyBirthrightRecruit = self.rng.choice(['Sakura', 'Kaze', 'Subaki', 'Hana'])
        self.earlyConquestRecruit = self.rng.choice(['Elise', 'Silas', 'Arthur', 'Effie'])

        if self.earlyConquestRecruit in self.MALE_CHARACTERS:
            self.CONQUEST_STAFF_CLASSES = self.MALE_STAFF_CLASSES
        else:
            self.CONQUEST_STAFF_CLASSES = self.FEMALE_STAFF_CLASSES

        if self.earlyBirthrightRecruit in self.MALE_CHARACTERS:
            self.BIRTHRIGHT_STAFF_CLASSES = self.MALE_STAFF_CLASSES
        else:
            self.BIRTHRIGHT_STAFF_CLASSES = self.FEMALE_STAFF_CLASSES

        if self.gameRoute == 'Birthright':
            self.ROUTE_CHARACTERS = self.BIRTHRIGHT_CHARACTERS
        elif self.gameRoute == 'Conquest':
            self.ROUTE_CHARACTERS = self.CONQUEST_CHARACTERS
        elif self.gameRoute == 'Revelations':
            self.ROUTE_CHARACTERS = self.REVELATION_CHARACTERS
        elif self.gameRoute == '':
            self.ROUTE_CHARACTERS = self.ALL_CHARACTERS

        if self.gameRoute == "Birthright":
            self.PMU_CHARACTERS = [
                'Felicia', 'Jakob', 'Kaze', 'Rinkah', 'Azura', 'Sakura', 'Hana', 'Subaki',
                'Silas', 'Saizo', 'Orochi', 'Mozu', 'Hinoka', 'Azama', 'Setsuna',
                'Hayato', 'Oboro', 'Hinata', 'Takumi', 'Kagero', 'Reina', 'Kaden', 'Ryoma',
                'Scarlet'
            ]
        elif self.gameRoute == "Conquest":
            self.PMU_CHARACTERS = [
                'Felicia', 'Jakob', 'Elise', 'Silas', 'Arthur', 'Effie', 'Mozu',
                'Odin', 'Niles', 'Azura', 'Nyx', 'Camilla', 'Selena', 'Beruka', 'Kaze',
                'Laslow', 'Peri', 'Benny', 'Charlotte', 'Leo', 'Keaton', 'Xander'
            ]
        else:
            self.PMU_CHARACTERS = [
                'Azura', 'Felicia', 'Jakob', 'Mozu', 'Sakura', 'Hana',
                'Subaki', 'Kaze', 'Rinkah', 'Takumi', 'Oboro', 'Hinata',
                'Saizo', 'Orochi', 'Reina', 'Kagero', 'Camilla', 'Selena', 'Beruka',
                'Kaden', 'Keaton', 'Elise', 'Arthur', 'Effie', 'Charlotte', 'Benny',
                'Silas', 'Shura', 'Nyx', 'Hinoka', 'Azama', 'Setsuna', 'Ryoma',
                'Leo', 'Xander', 'Odin', 'Niles', 'Laslow', 'Peri',
            ]

        self.PMUList = self.selectPMUCharacters()

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
        if self.rng.choice(2) == 1:  # 50% chance of uniform adjustment, 50% chance of proportional
            probas = self.addmax(np.asarray(growths) + 5)  # add a 5 growth rate to everything just for variance's sake
        else:
            probas = self.addmax(np.ones(8))
        if self.randomizeStatsAndGrowthsSum:
            newGrowthsSum = self.growthsSumMin + 10 * self.rng.choice((self.growthsSumMax-self.growthsSumMin+10)//10)
            newBaseStatsSum = self.baseStatsSumMin + self.rng.choice(self.baseStatsSumMax-self.baseStatsSumMin+1)
            baseStatCap = self.baseStatCap
            # if characterData["SwitchingCharacterName"] in ["Shura", "Izana", "Reina", "Camilla", "Leo", "Fuga"]: # prepromotes have higher base stats  # actually, they're good enough without this
            if characterData["SwitchingCharacterName"] in ["Camilla"]:  # Camilla deserves the buff to be equivalent to its vanilla counterpart
                newBaseStatsSum += 10
                baseStatCap += 3
            while growthsSum < newGrowthsSum:
                growthProbas = np.copy(probas)
                s = self.rng.choice(8, p=growthProbas)
                if growths[s] < self.growthCap:
                    growths[s] += 5
                    growthsSum += 5
                else:
                    growthProbas[s] = 0
                    growthProbas = self.addmax(growthProbas)
            while growthsSum > newGrowthsSum:
                s = self.rng.choice(np.where(growths>0)[0])
                growths[s] -= 5
                growthsSum -= 5
            while baseStatsSum < newBaseStatsSum:
                statProbas = np.copy(probas)
                t = self.rng.choice(8, p=statProbas)
                if baseStats[t] < self.baseStatCap:
                    baseStats[t] += 1
                    baseStatsSum += 1
                else:
                    statProbas[t] = 0
                    statProbas = self.addmax(statProbas)
            while baseStatsSum > newBaseStatsSum:
                t = self.rng.choice(np.where(baseStats>0)[0])
                baseStats[t] -= 1
                baseStatsSum -= 1
        else:
            baseStatsSumMax = self.baseStatsSumMax
            if characterData["SwitchingCharacterName"] in ["Shura", "Izana", "Reina", "Camilla", "Leo", "Fuga"]: # prepromotes have higher base stats
                baseStatsSumMax += 15
            if growthsSum < self.growthsSumMin or self.forceStatDecrease:
                while growthsSum < self.growthsSumMin:
                    s = self.rng.choice(8, p=probas)
                    if growths[s] < self.growthCap:
                        growths[s] += 5
                        growthsSum += 5
                    else:
                        probas[s] = 0
                        probas = self.addmax(probas)
                while baseStatsSum > baseStatsSumMax:
                    t = self.rng.choice(np.where(baseStats>0)[0])
                    baseStats[t] -= 1
                    baseStatsSum -= 1
            if self.forceStatIncrease:
                while baseStatsSum < self.baseStatsSumMin:
                    t = self.rng.choice(8, p=probas)
                    baseStats[t] += 1
                    baseStatsSum += 1
        characterData['Growths'] = growths
        characterData['BaseStats'] = baseStats
        if self.verbose:
            print("{}, {}, {}, {}, {}, {}".format(characterData['Name'], characterData['SwitchingCharacterName'], newGrowthsSum, newBaseStatsSum, growths, baseStats))
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

    # def computeBaseStats(self, characterName):
    #     """ returns the lvl 1 stats of the character """
    #
    #     characterStats = self.readCharacterStats(characterName)
    #     characterGrowths = self.readCharacterGrowths(characterName)
    #
    #     level = self.readCharacterLevel(characterName)
    #     promotionLevel = self.readCharacterPromotionLevel(characterName)
    #     baseClass = self.readCharacterBaseClass(characterName)
    #     originalClass = self.readCharacterOriginalClass(characterName)
    #     baseClassGrowths = self.readClassGrowths(baseClass)
    #     originalClassGrowths = self.readClassGrowths(originalClass)
    #
    #     minusStats = np.zeros(8)
    #     if level > 1:
    #         minusStats += (characterGrowths + originalClassGrowths) * (level - 1)
    #     if promotionLevel > 1:
    #         minusStats += (characterGrowths + baseClassGrowths) * (promotionLevel - 1)
    #     minusStats = np.floor(minusStats/100)
    #
    #     characterBaseStats = characterStats - minusStats
    #
    #     return characterBaseStats

    # def computeNewStats(self, character):
    #     """ Returns the new stats of the character: base stats are
    #     scaled up to the new level with the new class growths """
    #
    #     characterName = self.readCharacterName(character)
    #     characterBaseStats = self.readCharacterBaseStats(characterName)
    #     characterGrowths = self.readCharacterGrowths(characterName)
    #
    #     switchingCharacterName = self.readSwitchingCharacterName(character)
    #     switchingCharacter = self.getCharacter(switchingCharacterName)
    #
    #     newLevel = self.readCharacterLevel(switchingCharacterName)  # rebalanceLevels / Revelations effects are inside the function call
    #     self.setCharacterLevel(switchingCharacter, newLevel)  # worst case: it does nothing
    #     newPromotionLevel = self.readCharacterPromotionLevel(switchingCharacterName)
    #     newClass = self.readClassName(character)
    #     newBaseClass = self.readBaseClass(newClass, characterName)
    #     newClassGrowths = self.readClassGrowths(newClass)
    #     newBaseClassGrowths = self.readClassGrowths(newBaseClass)
    #
    #     plusStats = np.zeros(8)
    #     if newLevel > 1:
    #         plusStats += (characterGrowths + newClassGrowths) * (newLevel - 1)
    #     if promotionLevel > 1:
    #         plusStats += (characterGrowths + newBaseClassGrowths) * (newPromotionLevel - 1)
    #     plusStats = np.around((plusStats-25)/100) # if decimal part is above 0.75, round to superior
    #
    #     characterNewStats = characterBaseStats + plusStats
    #
    #     return characterNewStats

    def dataToString(self, data):
        return ','.join(list(map(str, list(map(int, data)))))

    def fixCharacter(self, character):
        """ Fixes the switchingCharacter's data so that the character's model
        and values fit """
        characterName = self.readCharacterName(character)
        characterOriginal = character
        characterNameOriginal = self.readCharacterName(character)
        switchingCharacterName = self.readSwitchingCharacterName(character)
        switchingCharacter = self.getCharacter(switchingCharacterName)

        if self.disableModelSwitch:
            # all changes will actually concern the switching character, this character will be fixed
            # when it's the turn of its switched character
            character = switchingCharacter
            characterName = switchingCharacterName

        newLevel = self.readCharacterLevel(switchingCharacterName)  # rebalanceLevels / Revelations effects are inside the function call
        self.setCharacterLevel(switchingCharacter, newLevel)  # worst case: it does nothing
        newPromotionLevel = self.readCharacterPromotionLevel(switchingCharacterName)
        newClass = self.readClassName(character)
        newBaseClass = self.readBaseClass(newClass, characterName)

        if self.forceClassSpread:
            if switchingCharacterName in self.randomizedClasses.keys():
                newClass = self.randomizedClasses[switchingCharacterName]  # take the class of the switching character
                newBaseClass = self.readBaseClass(newClass, characterName)
                if newPromotionLevel > 0 or (switchingCharacterName in ['Jakob', 'Felicia']):
                    self.setCharacterClass(character, newClass)
                else:
                    if self.forceStaffEarlyRecruit:
                        if switchingCharacterName == self.earlyConquestRecruit:
                            if newClass in ['Onmyoji', 'Priestess', 'Great Master']:
                                if self.earlyConquestRecruit in self.MALE_CHARACTERS:
                                    self.setCharacterClass(character, 'Monk')
                                if self.earlyConquestRecruit in self.FEMALE_CHARACTERS:
                                    self.setCharacterClass(character, 'Shrine Maiden')
                            else:
                                self.setCharacterClass(character, 'Troubadour')
                        elif switchingCharacterName == self.earlyBirthrightRecruit:
                            if newClass in ['Onmyoji', 'Priestess', 'Great Master']:
                                if self.earlyConquestRecruit in self.MALE_CHARACTERS:
                                    self.setCharacterClass(character, 'Monk')
                                if self.earlyConquestRecruit in self.FEMALE_CHARACTERS:
                                    self.setCharacterClass(character, 'Shrine Maiden')
                            else:
                                self.setCharacterClass(character, 'Troubadour')
                        elif self.limitStaffClasses and newBaseClass in ['Troubadour', 'Shrine Maiden', 'Monk']:
                            self.setCharacterReclassOne(character, newBaseClass)
                            if newClass == 'Great Master':
                                newBaseClass = self.rng.choice(['Spear Fighter', 'Sky Knight', 'Knight'])
                            elif newClass == 'Priestess':
                                newBaseClass = self.rng.choice(['Archer', 'Outlaw', 'Apothecary'])
                            elif newClass == 'Onmyoji':
                                newBaseClass = 'Diviner'
                            elif newClass == 'Strategist':
                                newBaseClass = self.rng.choice(['Diviner', 'Dark Mage'])
                            elif newClass in ['Maid', 'Butler']:
                                newBaseClass = 'Ninja'
                            else:
                                raise NotImplementedError("Missing non staff base class for class {}".format(newClass))
                        self.setCharacterClass(character, newBaseClass)
            else:
                pass  # character not in route

        else:
            # Staff Early Recruit Check
            if self.forceStaffEarlyRecruit:
                if switchingCharacterName == self.earlyConquestRecruit:
                    staffClassSet = self.CONQUEST_STAFF_CLASSES
                    staffClass = self.rng.choice(staffClassSet)
                    if staffClass in ['Onmyoji', 'Priestess', 'Great Master']:
                        if self.earlyConquestRecruit in self.MALE_CHARACTERS:
                            self.setCharacterClass(character, 'Monk')
                        if self.earlyConquestRecruit in self.FEMALE_CHARACTERS:
                            self.setCharacterClass(character, 'Shrine Maiden')
                    else:
                        self.setCharacterClass(character, 'Troubadour')
                elif switchingCharacterName == self.earlyBirthrightRecruit:
                    staffClassSet = self.BIRTHRIGHT_STAFF_CLASSES
                    staffClass = self.rng.choice(staffClassSet)
                    if staffClass in ['Onmyoji', 'Priestess', 'Great Master']:
                        if self.earlyConquestRecruit in self.MALE_CHARACTERS:
                            self.setCharacterClass(character, 'Monk')
                        if self.earlyConquestRecruit in self.FEMALE_CHARACTERS:
                            self.setCharacterClass(character, 'Shrine Maiden')
                    else:
                        self.setCharacterClass(character, 'Troubadour')

            # Staff Retainer Check
            if self.forceStaffRetainer:
                if switchingCharacterName in ['Jakob', 'Felicia']:
                    staffClassSet = self.JAKOB_CLASSES
                    if switchingCharacterName == 'Felicia':
                        staffClassSet = self.FELICIA_CLASSES
                    staffClass = self.rng.choice(staffClassSet)
                    self.setCharacterClass(character, staffClass)

            # Songstress Check
            if self.forceSongstress:
                if switchingCharacterName == 'Azura':
                    self.setCharacterClass(character, 'Songstress')

        # Villager Check
        if self.forceVillager:
            if switchingCharacterName == 'Mozu':
                self.setCharacterClass(character, 'Villager')


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
        self.addVarianceToData(characterData['BaseStats'], characterData['Growths'], characterData['Modifiers'])

        # Swap Stats
        self.swapCharacterLck(characterData)
        self.swapCharacterDefRes(characterData)
        self.swapCharacterSklSpd(characterData)
        self.swapCharacterStrMag(characterData)
        self.swapCharacterAtkDef(characterData)  # last

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
        plusStats = np.around((plusStats-25)/100) # if decimal part is above 0.75, round to superior
        characterNewStats = characterBaseStats + plusStats
        characterData['OldStats'] = characterData['Stats']
        characterData['Stats'] = characterNewStats
        # characterData['Stats'] = characterData['BaseStats']  # test

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

        # Increase Modifiers
        self.increaseModifiers(characterData['Modifiers'])

        # Set Data
        self.setCharacterStats(switchingCharacter, characterData['Stats'])
        self.setCharacterGrowths(switchingCharacter, characterData['Growths'])
        if self.forceViableCharacters:
            if switchingCharacterName not in self.PMUList:
                self.setCharacterGrowths(switchingCharacter, np.array([0, 0, 0, 0, 0, 0, 0, 0]))

        self.setCharacterModifiers(switchingCharacter, characterData['Modifiers'])

        # Randomize Skills
        self.randomizeSkills(switchingCharacter, characterName, newClass)

        if self.disableModelSwitch:
            self.setSwitchingCharacterName(characterOriginal, characterNameOriginal)

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

        characters = self.ROUTE_CHARACTERS.copy()

        classes = self.FINAL_CLASSES.copy()
        classes.pop(classes.index(self.randomizedClasses['Corrin']))
        classesBis = self.FINAL_CLASSES.copy()
        classesBis.pop(classesBis.index('Songstress'))  # one Songstress max
        classes = classes + classesBis
        classes = classes[:max(len(classesBis), len(characters))]

        # Staff Early Recruit Check
        staffClass = ''
        staffClass2 = ''
        if self.forceStaffEarlyRecruit:
            if self.earlyConquestRecruit in characters:
                staffClass = self.rng.choice(self.CONQUEST_STAFF_CLASSES)
                self.randomizedClasses[self.earlyConquestRecruit] = staffClass
                characters.pop(characters.index(self.earlyConquestRecruit))
                if staffClass in classes:
                    classes.pop(classes.index(staffClass))
            if self.earlyBirthrightRecruit in characters:
                staffClass2 = self.rng.choice(self.BIRTHRIGHT_STAFF_CLASSES)
                if self.earlyConquestRecruit in characters:
                    while staffClass2 == staffClass:
                        staffClass2 = self.rng.choice(self.BIRTHRIGHT_STAFF_CLASSES)
                self.randomizedClasses[self.earlyBirthrightRecruit] = staffClass2
                characters.pop(characters.index(self.earlyBirthrightRecruit))
                if staffClass2 in classes:
                    classes.pop(classes.index(staffClass2))

        # Staff Retainer Check
        if self.forceStaffRetainer:
            jakobClass = self.rng.choice(self.JAKOB_CLASSES)
            if self.forceStaffEarlyRecruit:
                while jakobClass in [staffClass, staffClass2]:
                    jakobClass = self.rng.choice(self.JAKOB_CLASSES)
            feliciaClass = self.rng.choice(self.FELICIA_CLASSES)
            if self.forceStaffEarlyRecruit:
                while feliciaClass in [staffClass, staffClass2, jakobClass]:
                    feliciaClass = self.rng.choice(self.FELICIA_CLASSES)
            self.randomizedClasses['Jakob'] = jakobClass
            self.randomizedClasses['Felicia'] = feliciaClass
            characters.pop(characters.index('Jakob'))
            characters.pop(characters.index('Felicia'))
            if jakobClass in classes:
                classes.pop(classes.index(jakobClass))
            if feliciaClass in classes:
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
            classes = classes[:len(characters)]

        for i, className in enumerate(classes):
            self.randomizedClasses[characters[i]] = className

        return None

    def randomizeSkills(self, switchingCharacter, characterName, className):
        switchingCharacterName = self.readCharacterName(switchingCharacter)
        nSkills = self.nSkills
        if self.nSkills == -1:
            skills = self.readSkills(switchingCharacter)
            nSkills = len(np.nonzero(skills)[0])
        skills = self.sampleSkills(nSkills, className)
        if characterName == 'Mozu':
            if self.forceMozuAptitude:
                if 108 not in skills:
                    skills[0] = 108

        if switchingCharacterName in ["Felicia", "Jakob"]:
            if self.forceLiveToServe:
                if 100 not in skills:
                    skills[2] = 100
        if switchingCharacterName == 'Mozu':
            if self.forceVillager or self.forceParalogueAptitude:
                if 108 not in skills:
                    skills[0] = 108
        elif switchingCharacterName == 'Niles':
            if self.forceLocktouch:
                if 112 not in skills:
                    skills[0] = 112
        elif switchingCharacterName == 'Kaze':
            if self.forceLocktouch:
                if 112 not in skills:
                    skills[0] = 112

        if self.PMUMode:
            if switchingCharacterName not in self.PMUList:
                if 149 not in skills:  # Survey skill, for identification
                    skills[-1] = 149

        return self.setCharacterSkills(switchingCharacter, skills)

    def readBaseClass(self, className, characterName):
        """ Returns a possible base class for a promoted class
            or the same class for an unpromoted one """
        baseClasses = self.classData[className]['BaseClasses']
        if className in ['Nohr Noble', 'Hoshido Noble', 'Grandmaster']:
            if className == 'Grandmaster' and not self.enableDLCBaseClass:
                return 'Grandmaster'
            else:
                if characterName in self.MALE_CHARACTERS:
                    return 'Nohr Prince'
                elif characterName in self.FEMALE_CHARACTERS:
                    return 'Nohr Princess'
                else:
                    raise ValueError('Character named "{}" not found in MALE_CHARACTERS or FEMALE_CHARACTERS'.format(characterName))
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
        if self.gameRoute == 'Conquest' and characterName == 'Kaze':
            return 9  # otherwise he stays at level 3
        if self.rebalanceLevels:
            if self.gameRoute == 'Revelations':
                return self.allCharacterData[characterName]['RebalancedRevelationsLevel']
            else:
                return self.allCharacterData[characterName]['RebalancedLevel']
        else:
            if self.gameRoute == 'Revelations':
                return self.allCharacterData[characterName]['RevelationsLevel']
            else:
                return self.allCharacterData[characterName]['Level']

    def readCharacterOriginalClass(self, characterName):
        return self.allCharacterData[characterName]['OriginalClass']

    def readCharacterPromotionLevel(self, characterName):
        return self.allCharacterData[characterName]['PromotionLevel']

    def readCharacterStats(self, characterName):
        return np.copy(self.allCharacterData[characterName]['Stats'])

    def readClassAttackType(self, className):
        return self.classData[className]['AttackType']

    def readClassDefenseType(self, className):
        return self.classData[className]['DefenseType']

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

    def sampleSkills(self, nSkills, className):
        """ Player-available skills: 1->112, 120->122, 128->159
        (147 skills total)
        Excludes Aptitude (108), Bold Stance (120), Point Blank (121), Winged Shield (122),
        Paragon (138), Armor Shield (139), Beast Shield (140), Taker Skills (142->148),
        Ballistician skills (149->152), Warp (154).
        Remaining Skills: 1->107, 109->112, 128->137, 141, 153, 155->159 (128 skills)
        Bookmarks: Draconic Hex (10), Luna (30), Strong Riposte (50), Tomefaire (70), Quixotic (90), Even Keel (128)"""
        baseSkills1 = [1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 36, 51, 53, 54, 57, 58, 89, 91, 99]
        baseSkills2 = [9, 20, 28, 39, 44, 45, 46, 47, 49, 50, 52, 73, 74, 76, 85, 86, 93, 101, 107, 109]
        promotedSkills1 = [10, 11, 12, 13, 16, 17, 18, 19, 21, 22, 25, 27, 29, 30, 31, 32, 35, 41, 59, 60, 64, 71, 77, 87, 88, 94, 95, 96, 100, 102, 104, 105]
        promotedSkills2 = [33, 34, 37, 38, 42, 43, 48, 55, 56, 61, 62, 63, 65, 66, 67, 68, 69, 70, 75, 78, 79, 80, 81, 82, 83, 84, 90, 97, 98, 103, 111]
        dlcBaseSkills1 = [128, 132, 134, 141, 156, 158]
        dlcBaseSkills2 = [72, 92, 129, 135, 153, 159]
        dlcPromotedSkills1 = [23, 26, 130, 136, 157]
        dlcPromotedSkills2 = [110, 133, 137, 155]
        dlcSkills = [120, 121, 122, 131, 139, 140, 142, 143, 144, 145, 146, 147, 148] # put 131, 142 and 145 (Aggressor, Strengthtaker and Speedtaker) here since they are kinda busted
        specificSkills = [24, 40, 106, 108, 112, 138, 149, 150, 151, 152, 154] # Inspiring Song (24), Beastbane (40), Foreign Princess (78), Nobility (106), Aptitude (108), Locktouch (112), Paragon (138), Ballistician skills (149->152) and Warp (154)

        if self.banDLCClassSkills:
            allBaseSkills1 = baseSkills1
            allBaseSkills2 = baseSkills2
            allPromotedSkills1 = promotedSkills1
            allPromotedSkills2 = promotedSkills2
        else:
            allBaseSkills1 = baseSkills1 + dlcBaseSkills1
            allBaseSkills2 = baseSkills2 + dlcBaseSkills2
            allPromotedSkills1 = promotedSkills1 + dlcPromotedSkills1
            allPromotedSkills2 = promotedSkills2 + dlcPromotedSkills2

        allSkills = allBaseSkills1 + allBaseSkills2 + allPromotedSkills1 + allPromotedSkills2

        if self.allowDLCSkills:
            allSkills += dlcSkills

        if self.disableBalancedSkillRandomization:
            skills = self.rng.choice(allSkills, 5, replace=False)
        else:
            skills = []
            skills.append(self.rng.choice(allBaseSkills1))
            skills.append(self.rng.choice(allBaseSkills2))
            skills.append(self.rng.choice(allPromotedSkills1))
            skills.append(self.rng.choice(allPromotedSkills2))
            lastSkill = skills[0]
            while lastSkill in skills:
                lastSkill = self.rng.choice(allSkills)
            skills.append(lastSkill)

            # Str/Mag +2
            if skills[0] == 3 and self.readClassAttackType(className) == 'Str':
                skills[0] = 2
            if skills[0] == 2 and self.readClassAttackType(className) == 'Mag':
                skills[0] = 3

            # Def/Res +2
            if skills[0] == 8 and self.readClassDefenseType(className) == 'Def':
                skills[0] = 7
            if skills[0] == 7 and self.readClassDefenseType(className) == 'Res':
                skills[0] = 8

            # Shadowgift
            if skills[0] == 141 and not className in self.TOME_CLASSES:
                while skills[0] == 141:
                    skills[0] = self.rng.choice(allBaseSkills1)

            # Live to Serve
            if skills[2] == 100 and not (className in self.FELICIA_CLASSES or className in self.JAKOB_CLASSES):
                while skills[2] == 100:
                    skills[2] = self.rng.choice(allPromotedSkills1)

            for i in [3, 4]:
                # Faire skills
                if skills[i] >= 65 and skills[i] <= 70:
                    weapon = self.rng.choice(self.classData[className]["Weapons"])
                    if weapon not in ["Staff", "Beaststone"]:
                        if className not in ["Swordmaster", "Spear Master", "Berserker", "Onmyoji", "Sniper", "MasterNinja", "Lodestar"]:
                            skills[i] = self.FAIRE_SKILLS[weapon]
                        else:
                            skills[i] = self.BREAKER_SKILLS[weapon]
                    else:
                        while skills[i] >= 65 and skills[i] <= 70:
                            skills[i] = self.rng.choice(allPromotedSkills2)

                # Breaker skills
                if skills[i] >= 79 and skills[i] <= 84:
                    weapon = self.rng.choice(self.classData[className]["Weapons"])
                    if weapon not in ["Staff", "Beaststone"]:
                        if className not in ["Wyvern Lord", "Blacksmith", "Hero", "Maid", "Butler", "Sorcerer", "Bow Knight", "Vanguard", "Dread Fighter"]:
                            skills[i] = self.BREAKER_SKILLS[weapon]
                        else:
                            skills[i] = self.FAIRE_SKILLS[weapon]
                    else:
                        while skills[i] >= 79 and skills[i] <= 84:
                            skills[i] = self.rng.choice(allPromotedSkills2)

        for i in range(nSkills, 5):  # erase added skills if needed
            skills[i] = 0

        return skills

    def selectPMUCharacters(self):
        characters = self.PMU_CHARACTERS.copy()
        PMUList = ['Corrin', 'Azura']
        characters.remove('Azura')
        if self.rng.random() < 0.5:
            PMUList.append('Jakob')
        else:
            PMUList.append('Felicia')
        characters.remove('Jakob')
        characters.remove('Felicia')
        if self.gameRoute == 'Conquest':
            PMUList.append(self.earlyConquestRecruit)
            characters.remove(self.earlyConquestRecruit)
        else:
            PMUList.append(self.earlyBirthrightRecruit)
            characters.remove(self.earlyBirthrightRecruit)
        n = len(characters) + 1
        benford = np.log(1+1/np.arange(1,n)) / np.log(n)
        PMUList = PMUList + self.rng.choice(characters, 12, replace=False, p=benford).tolist()
        return PMUList

    def setCharacterBitflags(self, character, bitflags):
        character['Bitflags']['@values'] = self.dataToString(bitflags)
        return character

    def setCharacterClass(self, character, className):
        character['ClassData']['@class'] = className
        return character

    def setCharacterGrowths(self, character, growths):
        character['Growths']['@values'] = self.dataToString(growths)
        return character

    def setCharacterLevel(self, character, level):
        character['LevelData']['@level'] = str(level)
        return character

    def setCharacterModifiers(self, character, modifiers):
        character['Modifiers']['@values'] = self.dataToString(modifiers)
        return character

    def setCharacterReclassOne(self, character, className):
        character['ClassData']['@reclassOne'] = className
        return character

    def setCharacterStats(self, character, stats):
        character['Stats']['@values'] = self.dataToString(stats)
        return character

    def setCharacterSkills(self, character, skills):
        character['Skills']['@values'] = self.dataToString(skills)
        return character

    def setSwitchingCharacterName(self, character, switchingCharacterName):
        character['StringData']['@switchingCharacter'] = switchingCharacterName
        return character

    def swapCharacterAtkDef(self, characterData):
        """
            swap Str/Mag (whichever is higher) with Def/Res (whichever is higher),
            assumes it is the last swap
        """

        stats = characterData['BaseStats']
        growths = characterData['Growths']
        modifiers = characterData['Modifiers']

        if stats[2] > stats[1] or (stats[2] == stats[1] and growths[2] > growths[1]):
            i = 2
        else:
            i = 1
        if stats[7] > stats[6] or (stats[7] == stats[6] and growths[7] > growths[6]):
            j = 7
        else:
            j = 6

        if self.rng.random() < self.swapAtkDefP:
            growths[i], growths[j] = growths[j], growths[i]
            stats[i], stats[j] = stats[j], stats[i]
            modifiers[i], modifiers[j] = modifiers[j], modifiers[i]

        return characterData

    def swapCharacterDefRes(self, characterData):
        "by default, def and res are according to class"

        className = characterData['NewClass']
        classDefenseType = self.readClassDefenseType(className)
        i, j = 6, 7  # default: 'Def'
        if classDefenseType == 'Res':
            i, j = 7, 6
        elif classDefenseType == 'Mixed':
            if self.rng.random() < 0.5:
                i, j = 7, 6
        elif classDefenseType != 'Def':
            raise ValueError("Defense type '{}' unknown".format(classDefenseType))

        growths = characterData['Growths']
        stats = characterData['BaseStats']
        modifiers = characterData['Modifiers']

        if growths[i] < growths[j]:
            growths[i], growths[j] = growths[j], growths[i]
        if stats[i] < stats[j]:
            stats[i], stats[j] = stats[j], stats[i]
        if modifiers[i] < modifiers[j]:
            modifiers[i], modifiers[j] = modifiers[j], modifiers[i]

        if self.rng.random() < self.swapDefResP:
            growths[i], growths[j] = growths[j], growths[i]
            stats[i], stats[j] = stats[j], stats[i]
            modifiers[i], modifiers[j] = modifiers[j], modifiers[i]

        if (characterData['SwitchingCharacterName'] == 'Gunter' and self.forceGunterDef) or (characterData['SwitchingCharacterName'] == 'Camilla' and self.forceCamillaDef):
            i, j = 6, 7
            if growths[i] < growths[j]:
                growths[i], growths[j] = growths[j], growths[i]
            if stats[i] < stats[j]:
                stats[i], stats[j] = stats[j], stats[i]
            if modifiers[i] < modifiers[j]:
                modifiers[i], modifiers[j] = modifiers[j], modifiers[i]

        return characterData

    def swapCharacterLck(self, characterData):
        s = self.rng.choice(7)
        if s == 5:  # Lck mapped to Res
            s = 7

        growths = characterData['Growths']
        stats = characterData['BaseStats']
        modifiers = characterData['Modifiers']

        if self.swapLckP < 0 or self.swapLckP > 1:
            threshold = growths[5]/100  # Lck Growth
            if self.rng.random() < threshold:
                if growths[5] > growths[s]:
                    growths[5], growths[s] = growths[s], growths[5]
                if stats[5] > stats[s]:
                    stats[5], stats[s] = stats[s], stats[5]
                if modifiers[5] > modifiers[s]:
                    modifiers[5], modifiers[s] = modifiers[s], modifiers[5]

        elif self.rng.random() < self.swapLckP:
            growths[5], growths[s] = growths[s], growths[5]
            stats[5], stats[s] = stats[s], stats[5]
            modifiers[5], modifiers[s] = modifiers[s], modifiers[5]

        return characterData

    def swapCharacterSklSpd(self, characterData):
        if self.rng.random() < self.swapSklSpdP:
            growths = characterData['Growths']
            growths[3], growths[4] = growths[4], growths[3]

            stats = characterData['BaseStats']
            stats[3], stats[4] = stats[4], stats[3]

            modifiers = characterData['Modifiers']
            modifiers[3], modifiers[4] = modifiers[4], modifiers[3]

        return characterData

    def swapCharacterStrMag(self, characterData):
        className = characterData['NewClass']
        if className == 'Basara':
            className = characterData['NewBaseClass']
        classAttackType = self.readClassAttackType(className)
        i, j = 1, 2  # default: 'Str'
        if classAttackType in ['Mag', 'MagMixed']:
            i, j = 2, 1
        elif classAttackType == 'Mixed':
            if self.rng.random() < 0.5:
                i, j = 2, 1
        elif classAttackType not in ['Str', 'StrMixed']:
            raise ValueError("Attack type '{}' unknown".format(classDefenseType))

        growths = characterData['Growths']
        stats = characterData['BaseStats']
        modifiers = characterData['Modifiers']

        if growths[i] < growths[j]:
            growths[i], growths[j] = growths[j], growths[i]
        if stats[i] < stats[j]:
            stats[i], stats[j] = stats[j], stats[i]
        if modifiers[i] < modifiers[j]:
            modifiers[i], modifiers[j] = modifiers[j], modifiers[i]

        # buffing the other atk stat
        if 'Mixed' in classAttackType:
            probas = np.ones(8)
            probas[i] = 0
            probas[j] = 0
            probas2 = np.copy(probas)
            for k in range(8):
                if stats[k] == 0:
                    probas[k] = 0
                if growths[k] == 0:
                    probas2[k] = 0
            probas = self.addmax(probas)
            probas2 = self.addmax(probas2)
            diff_stats = stats[i] - stats[j]
            diff_growths = growths[i] - growths[j]
            n_rounds_stats = self.rng.choice(diff_stats+1)
            n_rounds_growths = self.rng.choice(diff_growths//5 + 1)
            for _ in range(n_rounds_stats):
                s = self.rng.choice(8, p=probas)
                if stats[s] > 0:
                    stats[s] -= 1
                    stats[j] += 1
                else:
                    probas[s] = 0
                    probas = self.addmax(probas)

            for _ in range(n_rounds_growths):
                s = self.rng.choice(8, p=probas2)
                if growths[s] > 0:
                    growths[s] -= 5
                    growths[j] += 5
                else:
                    probas2[s] = 0
                    probas2 = self.addmax(probas2)

        if self.rng.random() < self.swapStrMagP:
            growths[i], growths[j] = growths[j], growths[i]
            stats[i], stats[j] = stats[j], stats[i]
            modifiers[i], modifiers[j] = modifiers[j], modifiers[i]

        return characterData

    def run(self):
        if self.gameRoute == 'Revelations':
            print("Note: Jakob, Felicia and Gunter remain at their recruitment spot in Revelations because of a level scaling issue.")
            print("Note: Hayato will not be replaced in Revelations due to a bug in the randomizer.")
            jakobCharacter = self.getCharacter('Jakob')
            jakobReplacement = self.getCharacter(self.readSwitchedCharacterName('Jakob'))
            self.setSwitchingCharacterName(jakobReplacement, self.readSwitchingCharacterName(jakobCharacter))
            self.setSwitchingCharacterName(jakobCharacter, 'Jakob')

            feliciaCharacter = self.getCharacter('Felicia')
            feliciaReplacement = self.getCharacter(self.readSwitchedCharacterName('Felicia'))
            self.setSwitchingCharacterName(feliciaReplacement, self.readSwitchingCharacterName(feliciaCharacter))
            self.setSwitchingCharacterName(feliciaCharacter, 'Felicia')

            gunterCharacter = self.getCharacter('Gunter')
            gunterReplacement = self.getCharacter(self.readSwitchedCharacterName('Gunter'))
            self.setSwitchingCharacterName(gunterReplacement, self.readSwitchingCharacterName(gunterCharacter))
            self.setSwitchingCharacterName(gunterCharacter, 'Gunter')

            hayatoCharacter = self.getCharacter('Hayato')
            hayatoReplacement = self.getCharacter(self.readSwitchedCharacterName('Hayato'))
            self.setSwitchingCharacterName(hayatoReplacement, self.readSwitchingCharacterName(hayatoCharacter))
            self.setSwitchingCharacterName(hayatoCharacter, 'Hayato')

        if self.forceClassSpread:
            with open('{}/ClassSpread.csv'.format(path), 'w') as fcsv:
                writer = csv.writer(fcsv, delimiter='\t')
                if self.PMUMode:
                    for name in [x for x in ['Corrin'] + self.ROUTE_CHARACTERS if x in self.PMUList]:
                        className = self.randomizedClasses[name]
                        row = [name, self.readSwitchedCharacterName(name), className]
                        writer.writerow(row)
                else:
                    for name in [x for x in ['Corrin'] + self.ROUTE_CHARACTERS if x in self.randomizedClasses.keys()]:
                        className = self.randomizedClasses[name]
                        row = [name, self.readSwitchedCharacterName(name), className]
                        writer.writerow(row)

        for character in self.settings['root']['Character']:
            self.fixCharacter(character)

        with open('{}/RandomizerSettingsUpdated.xml'.format(path), 'wb') as fxml:
            fxml.write(xmltodict.unparse(self.settings, pretty=True).encode('utf-8'))


## Run the randomizer

if __name__ == "__main__":
    fatesRandomizer = FatesRandomizer(
        allCharacterData,
        classData,
        settings,
        addmaxPow=args.addmax_pow,
        allowDLCSkills=args.allow_dlc_skills,
        banAmiiboCharacters=args.ban_amiibo_characters,
        banAnna=args.ban_anna,
        banBallistician=(not args.allow_ballistician),
        banChildren=args.ban_children,
        banDLCClasses=args.ban_dlc_classes,
        banDLCClassSkills=args.ban_dlc_class_skills,
        banWitch=args.ban_witch,
        baseStatCap=args.base_stat_cap,
        baseStatsSumMax=args.base_stats_sum_max,
        baseStatsSumMin=args.base_stats_sum_min,
        corrinClass=args.corrin_class,
        disableBalancedSkillRandomization=args.disable_balanced_skill_randomization,
        disableModelSwitch=args.disable_model_switch,
        enableDLCBaseClass=args.enable_dlc_base_class,
        enableGenderlessDLC=args.enable_genderless_dlc,
        forceClassSpread=(not args.disable_class_spread),
        forceCamillaDef=(not args.disable_camilla_def),
        forceGunterDef=(not args.disable_gunter_def),
        forceLiveToServe=(not args.disable_livetoserve),
        forceLocktouch=(not args.disable_locktouch),
        forceMozuAptitude=(args.enforce_mozu_aptitude),
        forceParalogueAptitude=args.enforce_paralogue_aptitude,
        forceStaffRetainer=(not args.disable_staff_retainer),
        forceStaffEarlyRecruit=(not args.disable_staff_early_recruit),
        forceStatDecrease=args.enforce_stat_decrease,
        forceStatIncrease=args.enforce_stat_increase,
        forceSongstress=(not args.disable_songstress),
        forceStrCorrin=(not args.enable_mag_only_corrin),
        forceSwordCorrin=args.enforce_sword_corrin,
        forceViableCharacters=args.enforce_viable_characters,
        forceVillager=args.enforce_villager,
        gameRoute=args.game_route,
        growthCap=args.growth_cap,
        growthP=args.growth_p,
        growthsSumMax=args.growths_sum_max,
        growthsSumMin=args.growths_sum_min,
        limitStaffClasses=args.enable_limit_staff_classes,
        modifierCoefficient=args.modifier_coefficient,
        modP=args.mod_p,
        nPasses=args.n_passes,
        nSkills=args.n_skills,
        PMUMode=args.pmu_mode,
        randomizeStatsAndGrowthsSum=(not args.disable_randomize_stats_growths_sum),
        rebalanceLevels=(not args.disable_rebalance_levels),
        seed=args.seed,
        statP=args.stat_p,
        swapAtkDefP=args.swap_atk_def_p,
        swapDefResP=args.swap_def_res_p,
        swapLckP=args.swap_lck_p,
        swapSklSpdP=args.swap_skl_spd_p,
        swapStrMagP=args.swap_str_mag_p,
        verbose=args.verbose
    )

    fatesRandomizer.run()
