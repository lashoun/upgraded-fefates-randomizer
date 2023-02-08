# -*- coding: utf-8 -*-

import xmltodict
import csv
import numpy as np
import argparse
from numpy.random import default_rng


## Initialize path and arguments

path = './data'

parser = argparse.ArgumentParser()
parser.add_argument('-asc', '--adjust-strategy-coeff', type=float, default=0.2, help="the lower the more uniform the stat/growth/mod randomization")
parser.add_argument('-ap', '--addmax-pow', type=float, default=0.7, help="the lower the more uniform growth adjustment")
parser.add_argument('-ab', '--allow-ballistician', action='store_true', help="allow Ballistician class in the randomization")
parser.add_argument('-ads', '--allow-dlc-skills', action='store_true', help="allow DLC skills in skill randomization")
parser.add_argument('-ba', '--ban-anna', action='store_true', help="ban Anna")
parser.add_argument('-bac', '--ban-amiibo-characters', action='store_true', help="ban Amiibo characters (Marth, Lucina, Robin, Ike)")
parser.add_argument('-bc', '--ban-children', action='store_true', help="ban children characters")
parser.add_argument('-bdc', '--ban-dlc-classes', action='store_true', help="ban DLC classes")
parser.add_argument('-bdcs', '--ban-dlc-class-skills', action='store_true', help="ban DLC class skills in skill randomization")
parser.add_argument('-bscap', '--base-stat-cap', type=int, default=8, help="if adjusting growths, max value for base stat")
parser.add_argument('-bssmax', '--base-stats-sum-max', type=int, default=25, help="if adjusting growths, decreasing stats sum to that value")
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
    'Ballistician', 'Witch', 'Lodestar', 'Vanguard', 'Great Lord', 'Grandmaster',
    'Enchanter', 'Warden'
],
                    default='', help="Corrin's final class", metavar="CORRIN_CLASS")
parser.add_argument('-dbsr', '--disable-balanced-skill-randomization', action='store_true', help="disable balanced skill randomization; skill randomization will be completely random")
parser.add_argument('-dcd', '--disable-camilla-def', action='store_true', help="disable Camilla's replacement's enforced higher Def than Res")
parser.add_argument('-dcs', '--disable-class-spread', action='store_true', help="disable diverse class reroll")
parser.add_argument('-dfu', '--disable-fates-upgraded', action='store_true', help="disables the assumption that you are playing Fates Upgraded; important for DLC class handling")
parser.add_argument('-dgd', '--disable-gunter-def', action='store_true', help="disable Gunter's replacement's enforced higher Def than Res")
parser.add_argument('-dlts', '--disable-livetoserve', action='store_true', help="disable the retainers' replacements' enforced Live to Serve skill")
parser.add_argument('-dl', '--disable-locktouch', action='store_true', help="disable Kaze and Niles' replacements' enforced Locktouch skill")
parser.add_argument('-dlsc', '--disable-limit-staff-classes', action='store_true', help="disables replacing staff only classes by offensive classes and setting the staff only class as a reclass option")
parser.add_argument('-dms', '--disable-model-switch', action='store_true', help="disable model switching but keep switching the rest of the data (stats, growths...)")
parser.add_argument('-dpc', '--debuff-prepromotes-coeff', type=int, default=0, help="percentage points of handicap for prepromote base stats")
parser.add_argument('-drl', '--disable-rebalance-levels', action='store_true', help="disable fairer level balance adjustments (reverts to levels from the original games)")
parser.add_argument('-drlu', '--disable-rng-level-ups', action='store_true', help="disable rng level ups; characters will have average stats w.r.t their growths")
parser.add_argument('-drr', '--def-res-ratio', type=float, default=0.8, help="ratio of higher def/res characters with mixed classes")
parser.add_argument('-drsgs', '--disable-randomize-stats-growths-sum', action='store_true', help="will disable randomizing stats and growths sum for each character between customizable bounds")
parser.add_argument('-ds', '--disable-songstress', action='store_true', help="disable Azura's replacement's enforced Songstress class")
parser.add_argument('-dsr', '--disable-staff-retainer', action='store_true', help="disable Jakob and Felicia's replacement's enforced healing class")
parser.add_argument('-dss', '--disable-staff-early-recruit', action='store_true', help="disable Sakura and/or Elise's replacement's enforced healing class")
parser.add_argument('-edbc', '--enable-dlc-base-class', action='store_true', help="will give unpromoted base classes to every DLC class for game balance (eg Ninja/Oni Savage for Dread Fighter)")
parser.add_argument('-egd', '--enable-genderless-dlc', action='store_true', help="allows DLC classes to be given regardless of gender. Will automatically trigger --enable-dlc-base-class since this will affect only unpromoted characters; prepromoted characters are banned from getting an illegal class since the randomizer doesn't support it")
parser.add_argument('-ema', '--enforce-mozu-aptitude', action='store_true', help="enforce Mozu (herself) having Aptitude")
parser.add_argument('-emoc', '--enable-mag-only-corrin', action='store_true', help="enables Corrin to get a Mag only class")
parser.add_argument('-epa', '--enforce-paralogue-aptitude', action='store_true', help="enforce Mozu's replacement to have Aptitude")
parser.add_argument('-erps', '--enable-randomized-personal-skills', action='store_true', help="will output recommended personal skills; you will have to manually edit them, e.g. using thane98's Paragon. Requires the `disable-class-spread` tag to NOT be passed")
parser.add_argument('-esc', '--enforce-sword-corrin', action='store_true', help="enforces Corrin to get a sword-wielding final class")
parser.add_argument('-esd', '--enforce-stat-decrease', action='store_true', help="enforces stat decrease to base stat sum max regardless of growth increase")
parser.add_argument('-esi', '--enforce-stat-increase', action='store_true', help="enforces stat increase to base stat sum min")
parser.add_argument('-ev', '--enforce-villager', action='store_true', help="enforce Mozu's replacement being a Villager with Aptitude")
parser.add_argument('-evc', '--enforce-viable-characters', action='store_true', help="will force you to play with only the first 15 characters encoutered by giving 0 growth rates to the others in the route; non-viable characters will be given the 'Survey' skill for easy identification")
parser.add_argument('-g', '--game-route', choices=['Revelations', 'Birthright', 'Conquest'], default='', help="game route, especially important to specify it if playing Revelations so that levels are the correct ones")
parser.add_argument('-gc', '--growth-cap', type=int, default=70, help="adjusted growths cap")
parser.add_argument('-gp', '--growth-p', type=float, default=1., help="probability of editing growths in a variability pass")
parser.add_argument('-gsmax', '--growths-sum-max', type=int, default=350, help="will adjust growths until sum is lower than specified value")
parser.add_argument('-gsmin', '--growths-sum-min', type=int, default=250, help="will adjust growths until sum is higher than specified value")
parser.add_argument('-ic', '--imposed-classes', type=lambda s: [item.strip() for item in s.split(',')], default=[], help='list of imposed classes separated by a comma')
parser.add_argument('-mc', '--modifier-coefficient', type=int, default=0, help="will increase all modifiers by specified coefficient")
parser.add_argument('-mp', '--mod-p', type=float, default=0.25, help="probability of editing modifiers in a variability pass")
parser.add_argument('-np', '--n-passes', type=int, default=10, help="number of variability passes (swap +/- 5 growths, +/- 1 stats and mods per pass")
parser.add_argument('-ns', '--n-skills', type=int, default=-1, choices=[-1, 0, 1, 2, 3, 4, 5], help="number of randomized skills; if -1, randomize existing skills")
parser.add_argument('-pmu', '--pmu-mode', action='store_true', help="`ClassSpread.csv` will only contain the 16 allowed characters for the run")
parser.add_argument('-rlp', '--rng-levelup-p', type=float, default=0.5, help="probability of a character having RNG level ups versus average level ups")
parser.add_argument('-s', '--seed', type=int, default=None, help="RNG seed")
parser.add_argument('-sp', '--stat-p', type=float, default=0.5, help="probability of editing stats in a variability pass")
parser.add_argument('-smap', '--str-mixed-attacker-p', type=float, default=0.1, help="probability of a character being a Str mixed character (positive Mag stat/growth/mod with pure Str class")
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
        weapons = row[13:16]
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
        addmaxPow=0.7,
        adjustStrategyCoeff=0.2,
        allowDLCSkills=False,
        banAmiiboCharacters=False,
        banAnna=False,
        banBallistician=True,
        banChildren=False,
        banDLCClasses=False,
        banDLCClassSkills=False,
        banWitch=False,
        baseStatCap=8,  # in adjustBaseStatsAndGrowths, max value for base stats
        baseStatsSumMax=25,  # in adjustBaseStatsAndGrowths, if growths have to be increased, will decrease stats sum to said value
        baseStatsSumMin=15,  # in adjustBaseStatsAndGrowths, will increase stats sum to said value
        corrinClass='',
        defResRatio=0.8,
        debuffPrepromotesCoeff=0,
        disableBalancedSkillRandomization=False,
        disableModelSwitch=False,  # will disable model switching
        enableDLCBaseClass=False,  # will give unpromoted base classes to every DLC class for game balance (eg Ninja/Oni Savage for Dread Fighter)
        enableGenderlessDLC=False,  # allows DLC classes to be given regardless of gender
        enableRandomizedPersonalSkills=False,  # output csv files will display recommended personal skills
        fatesUpgraded=True,  # important for DLC classes
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
        imposedClasses=None,
        limitStaffClasses=True,  # will limit staff only classes by putting characters in a magical class and offering the staff class as a possible reclass
        modifierCoefficient=0,  # value by which all modifiers will be increased
        modP=0.25,  # proba of editing modifiers in AddVariancetoData
        nPasses=10,  # number of passes in AddVariancetoData
        nSkills=-1,  # if -1, randomize existing skills
        PMUMode=False,  # ClassSpread.csv will contain only the 16 allowed characters, other characters will have the Survey skill
        randomizeStatsAndGrowthsSum=True,  # will sample a random value between min and max for each character
        rebalanceLevels=True,  # will rebalance recruitment levels
        rngLevelupP=0.5,
        seed=None,
        statP=0.5,  # proba of editing stats in AddVariancetoData
        strMixedAttackerP=0.1,  # probability of a character being a Str mixed attacker (positive Mag stat/growth with pure Str class)
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
        self.adjustStrategyCoeff = adjustStrategyCoeff
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
        self.debuffPrepromotesCoeff = debuffPrepromotesCoeff
        self.defResRatio = defResRatio
        self.disableBalancedSkillRandomization = disableBalancedSkillRandomization
        self.disableModelSwitch = disableModelSwitch
        self.enableDLCBaseClass = enableDLCBaseClass
        if enableGenderlessDLC and not enableDLCBaseClass:
            print("Note: enable-dlc-base-class will be enabled since it is required by enable-genderless-dlc: you will need to manually promote characters to their DLC class")
            self.enableDLCBaseClass = True
        self.enableGenderlessDLC = enableGenderlessDLC
        self.enableRandomizedPersonalSkills = enableRandomizedPersonalSkills
        self.fatesUpgraded = fatesUpgraded
        self.forceClassSpread = forceClassSpread
        if enableRandomizedPersonalSkills and not forceClassSpread:
            print("Note: disable-class-spread was passed so enable-randomized-personal-skills will be deactivated")
            self.enableRandomizedPersonalSkills = False
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
        self.imposedClasses = imposedClasses
        self.limitStaffClasses = limitStaffClasses
        self.modifierCoefficient = modifierCoefficient
        self.modP = modP
        self.nPasses = nPasses
        self.nSkills = nSkills
        self.PMUMode = PMUMode
        self.randomizeStatsAndGrowthsSum = randomizeStatsAndGrowthsSum
        self.rebalanceLevels = rebalanceLevels
        self.rngLevelupP = rngLevelupP
        self.rng = default_rng(seed)
        self.statP = statP
        self.strMixedAttackerP = strMixedAttackerP
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

        self.FELICIA_CLASSES = ['Onmyoji', 'Priestess',
                                'Falcon Knight', 'Adventurer', 'Strategist', 'Maid']
        self.JAKOB_CLASSES = ['Onmyoji', 'Great Master',
                              'Falcon Knight', 'Adventurer', 'Strategist', 'Butler']
        self.MALE_STAFF_CLASSES = ['Onmyoji', 'Strategist', 'Butler', 'Great Master']
        self.FEMALE_STAFF_CLASSES = ['Onmyoji', 'Priestess', 'Strategist', 'Maid']

        if self.enableGenderlessDLC:
            self.MALE_CLASSES = ['Great Master', 'Butler']
            self.FEMALE_CLASSES = ['Priestess', 'Maid']
        else:
            self.MALE_CLASSES = ['Great Master', 'Butler', 'Lodestar', 'Vanguard', 'Grandmaster', 'Ballistician']
            self.FEMALE_CLASSES = ['Priestess', 'Maid', 'Witch', 'Great Lord']
        self.TRUE_MALE_CLASSES = ['Great Master', 'Butler', 'Lodestar', 'Vanguard', 'Grandmaster', 'Ballistician']
        self.TRUE_FEMALE_CLASSES = ['Priestess', 'Maid', 'Witch', 'Great Lord']

        if self.fatesUpgraded:
            self.DLC_CLASSES = ['Ballistician']
        else:
            self.DLC_CLASSES = ['Dread Fighter', 'Dark Falcon', 'Ballistician',
                'Witch', 'Lodestar', 'Vanguard', 'Great Lord', 'Grandmaster']

        self.CUSTOM_CLASSES = ['Enchanter', 'Warden']

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

        if self.fatesUpgraded:
            self.FINAL_CLASSES += self.CUSTOM_CLASSES
            self.TOME_CLASSES += ['Enchanter']
            self.PROMOTED_CLASSES += self.CUSTOM_CLASSES

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
            'Laslow', 'Peri', 'Benny', 'Charlotte', 'Leo', 'Keaton', 'Xander',
            'Shura', 'Flora', 'Izana', 'Anna', 'Shigure', 'Dwyer', 'Sophie',
            'Midori', 'Siegbert', 'Forrest', 'Ignatius', 'Velouria', 'Percy',
            'Ophelia', 'Soleil', 'Nina', 'Marth', 'Lucina', 'Robin', 'Ike', 'Gunter'
        ]
        self.REVELATION_CHARACTERS = [
            'Azura', 'Felicia', 'Jakob', 'Mozu', 'Sakura', 'Hana',
            'Subaki', 'Kaze', 'Rinkah', 'Takumi', 'Oboro', 'Hinata',
            'Saizo', 'Orochi', 'Reina', 'Kagero', 'Camilla', 'Selena', 'Beruka',
            'Kaden', 'Keaton', 'Elise', 'Arthur', 'Effie', 'Charlotte', 'Benny',
            'Silas', 'Shura', 'Nyx', 'Hinoka', 'Azama', 'Setsuna', 'Ryoma',
            'Leo', 'Xander', 'Odin', 'Niles', 'Laslow', 'Peri', 'Flora', 'Fuga',
            'Anna', 'Shigure', 'Dwyer', 'Sophie', 'Midori', 'Shiro',
            'Kiragi', 'Asugi', 'Selkie', 'Hisame', 'Mitama', 'Caeldori', 'Rhajat',
            'Siegbert', 'Forrest', 'Ignatius', 'Velouria', 'Percy', 'Ophelia',
            'Soleil', 'Nina', 'Marth', 'Lucina', 'Robin', 'Ike', 'Gunter', 'Scarlet'
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
        self.PREPROMOTED_CHARACTERS = [
            'Camilla', 'Ryoma', 'Leo', 'Xander', 'Yukimura', 'Fuga',
            'Izana', 'Flora', 'Shura', 'Scarlet', 'Reina'
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

        self.PERSONAL_SKILLS = [
            'Supportive', 'Devoted Partner', 'Evasive Partner', 'Miraculous Save',
            'Healing Descant', 'Vow of Friendship', 'Highwayman', 'Peacebringer', 'Forager',
            'Fiery Blood', 'Quiet Strength', 'Fearsome Blow', 'Perfectionist', 'Pyrotechnics',
            'Capture', 'Rallying Cry', 'Divine Retribution', 'Optimist', 'Pride', 'Nohr Enmity',
            'Triple Threat', 'Competitive', 'Shuriken Mastery', 'Morbid Celebration',
            'Reciprocity', 'Bushido', 'In Extremis', 'Perspicacious', 'Forceful Partner',
            "Lily's Poise", 'Misfortunate', 'Puissance', 'Aching Blood', 'Kidnap', 'Countercurse',
            "Rose's Thorn", 'Fierce Rival', 'Opportunist', 'Fancy Footwork', 'Bloodthirst',
            'Fierce Mien', 'Unmask', 'Pragmatic', 'Collector', 'Chivalry', 'Icy Blood',
            'Draconic Heir', 'Born Steward', 'Perfect Pitch', 'Mischievous', 'Lucky Charm',
            'Noble Cause', 'Optimistic', 'Sweet Tooth', 'Playthings', 'Calm', 'Haiku', 'Prodigy',
            'Vendetta', 'Gallant', 'Fierce Counter', 'Guarded Bravery', 'Goody Basket',
            'Fortunate Son', 'Bibliophile', 'Sisterhood', 'Daydream',
            'Wind Disciple', 'Make a Killing'
        ]

        self.FILTERED_PERSONAL_SKILLS = [
            'Supportive', 'Quiet Strength', 'Perfectionist', 'Rallying Cry', 'Competitive',
            'Bushido', 'Perspicacious', "Lily's Poise", 'Puissance', "Rose's Thorns", 'Opportunist',
            'Bloodthirst', 'Chivalry', 'Draconic Heir', 'Playthings', 'Gallant', 'Fierce Counter',
            'Fortunate Son', 'Bibliophile', 'Sisterhood', 'Pragmatic'
        ]

        if self.gameRoute == 'Birthright':
            self.FILTERED_PERSONAL_SKILLS.append('Nohr Enmity')

        self.STRENGTH_PERSONAL_SKILLS = ['Puissance']
        self.MAGIC_PERSONAL_SKILLS = ['Bibliophile']
        self.DRAGON_PERSONAL_SKILLS = ['Draconic Heir']
        self.PARTNER_PERSONAL_SKILLS = ['Devoted Partner', 'Evasive Partner', 'Forceful Partner']
        self.SONGSTRESS_PERSONAL_SKILLS = ['Healing Descant', 'Quiet Strength', 'Rallying Cry', 'Perspicacious', "Lily's Poise", "Rose's Thorns", 'Fierce Mien', 'Fortunate Son']

        # if self.gameRoute == 'Birthright':
        #     self.allowedCharacters = [
        #     'Felicia', 'Jakob', 'Kaze', 'Rinkah', 'Azura', 'Sakura', 'Hana', 'Subaki',
        #     'Silas', 'Saizo', 'Orochi', 'Mozu', 'Hinoka', 'Azama', 'Setsuna', 'Oboro'
        # ]
        # elif self.gameRoute == 'Conquest':
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
                    self.MALE_CHARACTERS.remove(characterName)
                else:
                    self.FEMALE_CHARACTERS.remove(characterName)
                self.BIRTHRIGHT_CHARACTERS.remove(characterName)
                self.CONQUEST_CHARACTERS.remove(characterName)
                self.REVELATION_CHARACTERS.remove(characterName)
                self.ALL_CHARACTERS.remove(characterName)
        if self.banAnna:
            self.FEMALE_CHARACTERS.remove('Anna')
            self.BIRTHRIGHT_CHARACTERS.remove('Anna')
            self.CONQUEST_CHARACTERS.remove('Anna')
            self.REVELATION_CHARACTERS.remove('Anna')
            self.ALL_CHARACTERS.remove('Anna')
        if self.banChildren:
            for characterName in self.CHILDREN_CHARACTERS:
                if characterName in self.MALE_CHARACTERS:
                    self.MALE_CHARACTERS.remove(characterName)
                if characterName in self.FEMALE_CHARACTERS:
                    self.FEMALE_CHARACTERS.remove(characterName)
                if characterName in self.BIRTHRIGHT_CHARACTERS:
                    self.BIRTHRIGHT_CHARACTERS.remove(characterName)
                if characterName in self.CONQUEST_CHARACTERS:
                    self.CONQUEST_CHARACTERS.remove(characterName)
                self.REVELATION_CHARACTERS.remove(characterName)
                self.ALL_CHARACTERS.remove(characterName)

        if self.banDLCClasses:
            for className in self.DLC_CLASSES:
                if className in self.MALE_CLASSES:
                    self.MALE_CLASSES.remove(className)
                if className in self.FEMALE_CLASSES:
                    self.FEMALE_CLASSES.remove(className)
                if className in self.FINAL_CLASSES:
                    self.FINAL_CLASSES.remove(className)
                if className in self.PROMOTED_CLASSES:
                    self.PROMOTED_CLASSES.remove(className)
                if className in self.UNPROMOTED_CLASSES:
                    self.UNPROMOTED_CLASSES.remove(className)
                if className in self.MAGICAL_CLASSES:
                    self.MAGICAL_CLASSES.remove(className)
                if className in self.SWORD_CLASSES:
                    self.SWORD_CLASSES.remove(className)
        else:
            if self.banBallistician:
                if 'Ballicistian' in self.MALE_CLASSES:
                    self.MALE_CLASSES.remove('Ballistician')
                self.FINAL_CLASSES.remove('Ballistician')
                if 'Ballicistian' in self.UNPROMOTED_CLASSES:
                    self.UNPROMOTED_CLASSES.remove('Ballistician')
                elif 'Ballicistian' in self.PROMOTED_CLASSES:
                    self.PROMOTED_CLASSES.remove('Ballistician')
            if self.banWitch:
                if 'Witch' in self.FEMALE_CLASSES:
                    self.FEMALE_CLASSES.remove('Witch')
                self.FINAL_CLASSES.remove('Witch')
                if 'Witch' in self.UNPROMOTED_CLASSES:
                    self.UNPROMOTED_CLASSES.remove('Witch')
                elif 'Witch' in self.PROMOTED_CLASSES:
                    self.PROMOTED_CLASSES.remove('Witch')
                self.MAGICAL_CLASSES.remove('Witch')

        # Wrong noble classes disable supports with prepromoted units
        if self.gameRoute == "Birthright":
            self.FINAL_CLASSES.remove('Nohr Noble')
            self.PROMOTED_CLASSES.remove('Nohr Noble')
            self.SWORD_CLASSES.remove('Nohr Noble')
        elif self.gameRoute == 'Conquest':
            self.FINAL_CLASSES.remove('Hoshido Noble')
            self.PROMOTED_CLASSES.remove('Hoshido Noble')
            self.SWORD_CLASSES.remove('Hoshido Noble')

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
                'Silas', 'Nyx', 'Hinoka', 'Azama', 'Setsuna', 'Ryoma',
                'Leo', 'Xander', 'Odin', 'Niles', 'Laslow', 'Peri',
            ]

        self.PMUList = self.selectPMUCharacters()

        if self.forceClassSpread:
            self.randomizeAllClasses()

        if enableRandomizedPersonalSkills:
            self.randomizePersonalSkills()

    def addmax(self, x, p=None):
        if p is None:
            p = self.addmaxPow
        x = x**p
        return x / np.sum(x)

    def addVarianceToData(self, stats, growths, mods):
        """ Takes points from a given stat / growth / modifier and gives it to another """
        for _ in range(self.nPasses):
            i, j = self.rng.choice(8, 2, replace=False)
            x = self.rng.random()
            if x < self.growthP:
                if growths[j] >= 5 and growths[i] < self.growthCap:
                    growths[i] += 5
                    growths[j] -= 5
            if x < self.statP:
                if stats[j] >= 1 and stats[i] < self.baseStatCap:
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

        if self.rng.random() < self.adjustStrategyCoeff:  # adjustStrategyCoeff probability (default 0.2) of proportional adjustment, otherwise uniform. Only for growths, stats will always be uniform
            probas = self.addmax(np.asarray(growths) + 10)  # add a 10% growth to everything before normalization just for variance's sake
        else:
            probas = self.addmax(np.ones(8))

        if self.randomizeStatsAndGrowthsSum:
            newGrowthsSum = self.growthsSumMin + 10 * self.rng.choice((self.growthsSumMax-self.growthsSumMin+10)//10)
            newBaseStatsSum = self.baseStatsSumMin + self.rng.choice(self.baseStatsSumMax-self.baseStatsSumMin+1)
            baseStatCap = self.baseStatCap
            if characterData["SwitchingCharacterName"] == "Gunter":
                newGrowthsSum = 80  # nerf Gunter's replacement's growths
            # if characterData["SwitchingCharacterName"] in ["Shura", "Izana", "Reina", "Camilla", "Leo", "Fuga"]: # prepromotes have higher base stats  # actually, they're good enough without this
            # if characterData["SwitchingCharacterName"] in ["Reina", "Camilla"]:  # Reina and Camilla deserve the buff to be equivalent to their vanilla counterparts  # actually, removing it seems to be fine
                # newBaseStatsSum += 10
                # baseStatCap += 3
            if characterData["SwitchingCharacterName"] == "Mozu" and self.forceParalogueAptitude:
                newBaseStatsSum -= 10  # nerf Mozu's replacement's base stats
                newBaseStatsSum = max(newBaseStatsSum, 0)

            growthProbas = np.copy(probas)
            while growthsSum < newGrowthsSum:
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

            statProbas = self.addmax(np.ones(8))
            while baseStatsSum < newBaseStatsSum:
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
            # if characterData["SwitchingCharacterName"] in ["Shura", "Izana", "Reina", "Camilla", "Leo", "Fuga"]: # prepromotes have higher base stats
            # if characterData["SwitchingCharacterName"] in ["Camilla"]:  # Camilla deserves the buff to be equivalent to her vanilla counterpart
                # baseStatsSumMax += 10
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
                probas = self.addmax(np.ones(8))
                while baseStatsSum < self.baseStatsSumMin:
                    t = self.rng.choice(8, p=probas)
                    baseStats[t] += 1
                    baseStatsSum += 1
        characterData['Growths'] = growths
        characterData['BaseStats'] = baseStats

        if self.verbose:
            print("{}, {}, {}, {}, {}, {}".format(characterData['Name'], characterData['SwitchingCharacterName'], newGrowthsSum, newBaseStatsSum, growths, baseStats))

        return characterData

    def checkQuality(self, characterNames, classes):
        """ in place, ugly loop that ends only if:
            - no character has a gender-locked class of the wrong gender
            - no prepromoted character is a Hoshido Noble or Nohr Noble
            - Gunter and Camilla have a Def > Res class
        """
        assert len(characterNames) == len(classes), "characterNames and classes have different lengths: {} and {}".format(len(characterNames), len(classes))
        qualityPass = False
        while not qualityPass:
            qualityPass = True
            for i, className in enumerate(classes):
                characterName = characterNames[i]
                if (className in self.MALE_CLASSES or (className in self.TRUE_MALE_CLASSES and characterName in self.PREPROMOTED_CHARACTERS)) and characterName not in self.MALE_CHARACTERS:
                    newCharacterName = self.rng.choice([x for x in self.MALE_CHARACTERS if x in characterNames])
                    j = characterNames.index(newCharacterName)
                    classes[i], classes[j] = classes[j], classes[i]
                    qualityPass = False
                elif (className in self.FEMALE_CLASSES or (className in self.TRUE_FEMALE_CLASSES and characterName in self.PREPROMOTED_CHARACTERS)) and characterName not in self.FEMALE_CHARACTERS:
                    newCharacterName = self.rng.choice([x for x in self.FEMALE_CHARACTERS if x in characterNames])
                    j = characterNames.index(newCharacterName)
                    classes[i], classes[j] = classes[j], classes[i]
                    qualityPass = False
                elif className in ["Hoshido Noble", "Nohr Noble"] and characterName in self.PREPROMOTED_CHARACTERS:
                    newCharacterName = self.rng.choice([x for x in self.ROUTE_CHARACTERS if (x in characterNames and x not in self.PREPROMOTED_CHARACTERS)])
                    j = characterNames.index(newCharacterName)
                    classes[i], classes[j] = classes[j], classes[i]
                    qualityPass = False
                elif self.readClassDefenseType(className) != 'Def' and ((characterName == "Gunter" and self.forceGunterDef) or (characterName == "Camilla" and self.forceCamillaDef)):
                    newClass = self.rng.choice([x for x in classes if self.readClassDefenseType(x) == 'Def'])
                    j = classes.index(newClass)
                    classes[i], classes[j] = classes[j], classes[i]
                    qualityPass = False

        return characterNames, classes

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
        newPromotionLevel = self.readCharacterPromotionLevel(switchingCharacterName)
        newClass = self.readClassName(character)
        newBaseClass = self.readBaseClass(newClass, characterName)

        if self.forceClassSpread:
            if switchingCharacterName in self.randomizedClasses.keys():
                newClass = self.randomizedClasses[switchingCharacterName]  # take the class of the switching character
                newBaseClass = self.readBaseClass(newClass, characterName)
                if newPromotionLevel > 0 or (switchingCharacterName in ['Jakob', 'Felicia']):
                    # if switchingCharacterName == 'Reina' and self.gameRoute == 'Birthright':  # to prevent crash in Birthright  # spawn tile modified, should be ok now
                    #     self.setCharacterClass(character, 'Kinshi Knight')
                    #     self.setCharacterReclassOne(character, newBaseClass)
                    # else:
                    #     self.setCharacterClass(character, newClass)
                    if newClass == 'Enchanter':  # a heart seal will be needed
                        self.setCharacterClass(character, 'Adventurer')
                    elif newClass == 'Warden':  # a heart seal will be needed
                        self.setCharacterClass(character, 'General')
                    else:
                        self.setCharacterClass(character, newClass)
                else:
                    if self.forceStaffEarlyRecruit:
                        if switchingCharacterName == self.earlyConquestRecruit:
                            if newClass in ['Onmyoji', 'Priestess', 'Great Master']:
                                if switchingCharacterName in self.MALE_CHARACTERS:
                                    newBaseClass = 'Monk'
                                if switchingCharacterName in self.FEMALE_CHARACTERS:
                                    newBaseClass = 'Shrine Maiden'
                            else:
                                newBaseClass = 'Troubadour'
                        elif switchingCharacterName == self.earlyBirthrightRecruit:
                            if newClass in ['Onmyoji', 'Priestess', 'Great Master']:
                                if switchingCharacterName in self.MALE_CHARACTERS:
                                    newBaseClass = 'Monk'
                                if switchingCharacterName in self.FEMALE_CHARACTERS:
                                    newBaseClass = 'Shrine Maiden'
                            else:
                                newBaseClass = 'Troubadour'
                    if (not (self.forceStaffEarlyRecruit and switchingCharacterName in [self.earlyConquestRecruit, self.earlyBirthrightRecruit])) and self.limitStaffClasses and newBaseClass in ['Troubadour', 'Shrine Maiden', 'Monk']:
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
        self.adjustCharacterStrMag(characterData)
        self.swapCharacterAtkDef(characterData)  # last
        if switchingCharacterName in ['Jakob', 'Felicia']:
            self.swapRetainerStats(characterData)

        # Scale Stats to New Level
        characterBaseStats = characterData['BaseStats']
        characterGrowths = characterData['Growths']
        if characterName == 'Mozu' and self.forceMozuAptitude:
            characterGrowths = np.copy(characterGrowths) + 10
        plusStats = np.zeros(8)
        if self.rng.random() < self.rngLevelupP:
            if newLevel > 1:
                if newPromotionLevel > 1:
                    growths_temp = characterGrowths + newClassGrowths - self.debuffPrepromotesCoeff  # newClassGrowths
                    growths_temp = np.sum(growths_temp) * self.addmax(growths_temp)
                    for _ in range(newLevel - 1):
                        levelUpRNG = 100 * self.rng.random(8)
                        plusStats += levelUpRNG < growths_temp
                else:
                    growths_temp = characterGrowths + newBaseClassGrowths  # newBaseClassGrowths
                    growths_temp = np.sum(growths_temp) * self.addmax(growths_temp)
                    for _ in range(newLevel - 1):
                        levelUpRNG = 100 * self.rng.random(8)
                        plusStats += levelUpRNG < growths_temp
            if newPromotionLevel > 1:
                growths_temp = characterGrowths + newBaseClassGrowths - self.debuffPrepromotesCoeff
                growths_temp = np.sum(growths_temp) * self.addmax(growths_temp)
                for _ in range(newPromotionLevel - 1):
                    levelUpRNG = 100 * self.rng.random(8)
                    plusStats += levelUpRNG < growths_temp
        else:
            if newLevel > 1:
                if newPromotionLevel > 1:
                    growths_temp = characterGrowths + newClassGrowths - self.debuffPrepromotesCoeff
                    growths_temp = np.sum(growths_temp) * self.addmax(growths_temp)
                    plusStats += growths_temp * (newLevel - 1)
                else:
                    growths_temp = characterGrowths + newBaseClassGrowths
                    growths_temp = np.sum(growths_temp) * self.addmax(growths_temp)
                    plusStats += growths_temp * (newLevel - 1)
            if newPromotionLevel > 1:
                growths_temp = characterGrowths + newBaseClassGrowths - self.debuffPrepromotesCoeff
                growths_temp = np.sum(growths_temp) * self.addmax(growths_temp)
                plusStats += growths_temp * (newPromotionLevel - 1)
            plusStats = np.around((plusStats-25)/100) # if decimal part is above 0.75, round to superior
        characterNewStats = characterBaseStats + plusStats
        characterData['OldStats'] = characterData['Stats']
        characterData['Stats'] = characterNewStats
        # characterData['Stats'] = characterData['BaseStats']  # test

        if self.verbose:
            print("switchingCharacterName: {}".format(switchingCharacterName))
            print("newLevel, newPromotionLevel: {}, {}".format(newLevel, newPromotionLevel))
            print("OldStats: {}, total: {}".format(characterData['OldStats'], np.sum(characterData['OldStats'])))
            print("OldBaseStats: {}, total: {}".format(characterData['OldBaseStats'], np.sum(characterData['OldBaseStats'])))
            print("OldGrowths: {}, total: {}".format(characterData['OldGrowths'], np.sum(characterData['OldGrowths'])))
            print("Growths: {}, total: {} -> {}".format(characterData['Growths'], np.sum(characterData['OldGrowths']), np.sum(characterData['Growths'])))
            print("plusStats: {}, total: {}".format(plusStats, np.sum(plusStats)))
            print("BaseStats: {}, total: {} -> {}".format(characterData['BaseStats'], np.sum(characterData['OldBaseStats']), np.sum(characterData['BaseStats'])))
            print("Stats: {}, total: {} -> {}".format(characterData['Stats'], np.sum(characterData['OldStats']), np.sum(characterData['Stats'])))

        # Increase Modifiers
        self.increaseModifiers(characterData['Modifiers'])

        # Set Data
        if not (self.gameRoute == 'Birthright' and switchingCharacterName == "Reina") and newClass in self.DLC_CLASSES and newPromotionLevel > 0:
            # Reina has to stay Kinshi Knight when she comes so no need to adjust the level
            self.setCharacterLevel(switchingCharacter, newLevel + newPromotionLevel)
            self.setCharacterPromotionLevel(switchingCharacter, -1)
        else:
            self.setCharacterLevel(switchingCharacter, newLevel)
        self.setCharacterLevel(switchingCharacter, newLevel)
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
        characterNames = self.ROUTE_CHARACTERS.copy()
        if self.PMUMode:
            characterNames = self.PMUList.copy()
        removedCharacters = []

        if 'Corrin' in characterNames:
            characterNames.remove('Corrin')
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

        if self.corrinClass in self.imposedClasses:
            self.imposedClasses.remove(self.corrinClass)
        classes = [c for c in self.FINAL_CLASSES if c not in (self.imposedClasses + [self.corrinClass])]

        self.rng.shuffle(classes)
        classes2 = self.FINAL_CLASSES.copy()
        classes2.remove('Songstress')  # one Songstress max
        self.rng.shuffle(classes2)
        if self.rng.random() < 0.5:  # remove classes that are almost identical
            if 'Great Master' in classes:
                classes.remove('Great Master')
            if 'Priestess' in classes2:
                classes2.remove('Priestess')
            if 'Butler' in classes:
                classes.remove('Butler')
            if 'Maid' in classes2:
                classes2.remove('Maid')
        else:
            if 'Priestess' in classes:
                classes.remove('Priestess')
            if 'Great Master' in classes2:
                classes2.remove('Great Master')
            if 'Maid' in classes:
                classes.remove('Maid')
            if 'Butler' in classes2:
                classes2.remove('Butler')

        classes = self.imposedClasses + classes + classes2
        classes2 = classes[len(characterNames):]
        classes = classes[:len(characterNames)]

        # Staff Early Recruit Check
        staffClass = ''
        staffClass2 = ''
        if self.forceStaffEarlyRecruit:
            if self.gameRoute != "Birthright" and self.earlyConquestRecruit in characterNames:
                conquestStaffClasses = [c for c in self.CONQUEST_STAFF_CLASSES if c in classes]
                if len(conquestStaffClasses) == 0:
                    staffClass = self.rng.choice(self.CONQUEST_STAFF_CLASSES)
                else:
                    staffClass = self.rng.choice(conquestStaffClasses)
                self.randomizedClasses[self.earlyConquestRecruit] = staffClass
                characterNames.remove(self.earlyConquestRecruit)
                removedCharacters.append(self.earlyConquestRecruit)
                if staffClass in classes:
                    classes.remove(staffClass)
                else:
                    classes.remove(self.rng.choice([c for c in classes if c not in self.imposedClasses]))
            if self.gameRoute != "Conquest" and self.earlyBirthrightRecruit in characterNames:
                birthrightStaffClasses = [c for c in self.BIRTHRIGHT_STAFF_CLASSES if c in classes]
                if self.gameRoute != "Birthright" and self.earlyConquestRecruit in characterNames:
                    if staffClass in birthrightStaffClasses:
                        birthrightStaffClasses.remove(staffClass)
                if len(birthrightStaffClasses) == 0:
                    staffClass2 = self.rng.choice(self.BIRTHRIGHT_STAFF_CLASSES)
                else:
                    staffClass2 = self.rng.choice(birthrightStaffClasses)
                self.randomizedClasses[self.earlyBirthrightRecruit] = staffClass2
                characterNames.remove(self.earlyBirthrightRecruit)
                removedCharacters.append(self.earlyBirthrightRecruit)
                if staffClass2 in classes:
                    classes.remove(staffClass2)
                else:
                    classes.remove(self.rng.choice([c for c in classes if c not in self.imposedClasses]))

        # Staff Retainer Check
        if self.forceStaffRetainer:
            jakobClass = self.rng.choice(self.JAKOB_CLASSES)
            if self.forceStaffEarlyRecruit:
                jakobClasses = [c for c in self.JAKOB_CLASSES if (c not in [staffClass, staffClass2] and c in classes)]
                if len(jakobClasses) == 0:
                    jakobClasses = [c for c in self.JAKOB_CLASSES if c not in [staffClass, staffClass2]]
                jakobClass = self.rng.choice(jakobClasses)
            feliciaClass = self.rng.choice(self.FELICIA_CLASSES)
            if self.forceStaffEarlyRecruit:
                feliciaClasses = [c for c in self.FELICIA_CLASSES if (c not in [staffClass, staffClass2, jakobClass] and c in classes)]
                if len(feliciaClasses) == 0:
                    feliciaClasses = [c for c in self.FELICIA_CLASSES if c not in [staffClass, staffClass2]]
                feliciaClass = self.rng.choice(feliciaClasses)
            if 'Jakob' in characterNames:
                self.randomizedClasses['Jakob'] = jakobClass
                characterNames.remove('Jakob')
                removedCharacters.append('Jakob')
                if jakobClass in classes:
                    classes.remove(jakobClass)
                else:
                    classes.remove(self.rng.choice([c for c in classes if c not in self.imposedClasses]))
            if 'Felicia' in characterNames:
                self.randomizedClasses['Felicia'] = feliciaClass
                characterNames.remove('Felicia')
                removedCharacters.append('Felicia')
                if feliciaClass in classes:
                    classes.remove(feliciaClass)
                else:
                    classes.remove(self.rng.choice([c for c in classes if c not in self.imposedClasses]))

        # Songstress Check
        if self.forceSongstress and 'Azura' in characterNames:
            self.randomizedClasses['Azura'] = 'Songstress'
            characterNames.remove('Azura')
            removedCharacters.append('Azura')
            if 'Songstress' in classes:
                classes.remove('Songstress')
            else:
                    classes.remove(self.rng.choice([c for c in classes if c not in self.imposedClasses]))

        # Villager Check
        if self.forceVillager and 'Mozu' in characterNames:
            if self.fatesUpgraded:
                villagerPromotedClass = self.rng.choice(['Master of Arms', 'Great Lord'])
            else:
                villagerPromotedClass = self.rng.choice(['Master of Arms', 'Merchant'])
            self.randomizedClasses['Mozu'] = villagerPromotedClass
            characterNames.remove('Mozu')
            removedCharacters.append('Mozu')
            if villagerPromotedClass in classes:
                classes.remove(villagerPromoted)
            else:
                classes.remove(self.rng.choice([c for c in classes if c not in self.imposedClasses]))

        characterNames2 = [x for x in self.ROUTE_CHARACTERS if (x not in characterNames and x not in removedCharacters)]

        self.rng.shuffle(classes)
        self.checkQuality(characterNames, classes)
        if len(characterNames2) > 0:
            classes2 = classes2[:len(characterNames2)]
            self.rng.shuffle(classes2)
            self.checkQuality(characterNames2, classes2)

        # if self.banChildren:
        #     self.rng.shuffle(classes)
        #     classes = classes[:len(characterNames)]
        #     self.checkQuality(characterNames, classes)
        # else:  # prioritize variance in parent classes
        #     childrenStart = characterNames.index('Shigure')
        #     parentCharacterNames = characterNames[:childrenStart]
        #     childrenCharacterNames = characterNames[childrenStart:]
        #     parentClasses = classes[:childrenStart]
        #     childrenClasses = classes[childrenStart:]
        #     self.rng.shuffle(parentClasses)  # in place
        #     self.rng.shuffle(childrenClasses)  # in place
        #     self.checkQuality(parentCharacterNames, parentClasses)
        #     self.checkQuality(childrenCharacterNames, childrenClasses)
        #     classes = parentClasses + childrenClasses
        #     classes = classes[:len(characterNames)]

        for i, className in enumerate(classes):
            self.randomizedClasses[characterNames[i]] = className
        for i, className in enumerate(classes2):
            self.randomizedClasses[characterNames2[i]] = className

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

    def randomizePersonalSkills(self):
        partnerSkill = self.rng.choice(self.PARTNER_PERSONAL_SKILLS)
        personalSkills = self.FILTERED_PERSONAL_SKILLS.copy()
        self.rng.shuffle(personalSkills)
        azuraSkill = self.rng.choice(self.SONGSTRESS_PERSONAL_SKILLS)
        if azuraSkill in personalSkills:
            personalSkills.remove(azuraSkill)
        corrinSkill = self.rng.choice(personalSkills)
        personalSkills.remove(corrinSkill)
        self.rng.shuffle(personalSkills)
        personalSkillsBis = self.PERSONAL_SKILLS.copy()
        self.rng.shuffle(personalSkillsBis)
        peronsalSkillsBis = personalSkills[15:] + personalSkillsBis
        personalSkills = [partnerSkill] + personalSkills[:15].copy()
        self.rng.shuffle(personalSkills)
        personalSkills = [corrinSkill] + personalSkills + personalSkillsBis
        names = self.randomizedClasses.keys()
        if self.PMUMode:
            names2 = self.PMUList.copy()
            for name in names:
                if name not in names2:
                    names2.append(name)
            names = names2
        classes = [self.randomizedClasses[name] for name in names]
        if self.PMUMode:
            classes = classes[:len(self.PMUList)]
        personalSkillsBis = personalSkills[len(classes):].copy()
        personalSkills = personalSkills[:len(classes)]
        for i, className in enumerate(classes):  # ugly loops but it should virtually never fail
            while personalSkills[i] in self.STRENGTH_PERSONAL_SKILLS and 'Str' not in self.readClassAttackType(className):
                personalSkills[i] = personalSkillsBis.pop(0)
            while personalSkills[i] in self.MAGIC_PERSONAL_SKILLS and 'Mag' not in self.readClassAttackType(className):
                personalSkills[i] = personalSkillsBis.pop(0)
            while personalSkills[i] in self.DRAGON_PERSONAL_SKILLS and className not in self.DRAGON_CLASSES:
                personalSkills[i] = personalSkillsBis.pop(0)

        for i, className in enumerate(classes):
            if className in self.DRAGON_CLASSES:
                if 'Draconic Heir' not in personalSkills and self.rng.random() < 0.3 and personalSkills[i] not in self.PARTNER_PERSONAL_SKILLS:
                    personalSkills[i] = 'Draconic Heir'
            if className in self.TOME_CLASSES:
                if 'Bibliophile' not in personalSkills and self.rng.random() < 0.05 and personalSkills[i] not in self.PARTNER_PERSONAL_SKILLS:
                    personalSkills[i] = 'Bibliophile'
            if className not in self.MAGICAL_CLASSES:
                if 'Puissance' not in personalSkills and self.rng.random() < 0.02 and personalSkills[i] not in self.PARTNER_PERSONAL_SKILLS:
                    personalSkills[i] = 'Puissance'
            if className == 'Songstress':
                personalSkills[i] = azuraSkill

        personalSkills = personalSkills + personalSkillsBis

        self.personalSkills = {}
        for i, name in enumerate(names):
            self.personalSkills[name] = personalSkills[i]

    def readBaseClass(self, className, characterName):
        """ Returns a possible base class for a promoted class
            or the same class for an unpromoted one """
        baseClasses = self.classData[className]['BaseClasses']
        if className == 'Grandmaster' and not self.enableDLCBaseClass:
            return 'Grandmaster'
        elif className in ['Nohr Noble', 'Hoshido Noble'] or (className == 'Grandmaster' and not self.fatesUpgraded):
            if characterName in self.MALE_CHARACTERS:
                return 'Nohr Prince'
            elif characterName in self.FEMALE_CHARACTERS:
                return 'Nohr Princess'
            else:
                raise ValueError('Character named "{}" not found in MALE_CHARACTERS or FEMALE_CHARACTERS'.format(characterName))
        elif className == 'Onmyoji':
            if characterName in self.FEMALE_CHARACTERS:
                return 'Shrine Maiden'
            else:
                return 'Monk'
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
        if self.gameRoute == 'Conquest' and characterName == 'Shura':
            return 2  # he is recruited at level 10 in the other routes
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
        baseSkills2 = [9, 20, 28, 39, 44, 45, 46, 47, 49, 50, 52, 73, 74, 76, 85, 86, 93, 101, 109]
        promotedSkills1 = [10, 11, 12, 13, 16, 17, 18, 19, 21, 22, 25, 27, 29, 30, 31, 32, 35, 41, 59, 60, 64, 71, 77, 87, 88, 94, 95, 96, 100, 102, 104, 105]
        promotedSkills2 = [33, 34, 37, 38, 42, 43, 48, 56, 61, 62, 63, 65, 66, 67, 68, 69, 70, 75, 79, 80, 81, 82, 83, 84, 97, 98, 103, 111]
        if self.gameRoute == "Revelations":
            promotedSkills2.append(78)  # Foreign Princess
        dlcBaseSkills1 = [128, 132, 134, 141, 156, 158]
        dlcBaseSkills2 = [72, 92, 129, 135, 153, 159]
        dlcPromotedSkills1 = [23, 26, 130, 136, 157]
        dlcPromotedSkills2 = [110, 133, 137, 155]
        dlcSkills = [120, 121, 122, 131, 139, 140, 142, 143, 144, 145, 146, 147, 148] # put 131, 142 and 145 (Aggressor, Strengthtaker and Speedtaker) here since they are kinda busted
        specificSkills = [24, 40, 55, 78, 90, 106, 107, 108, 112, 138, 149, 150, 151, 152, 154] # Inspiring Song (24), Beastbane (40), Life And Death (55), Foreign Princess (78), Quixotic (90), Nobility (106), Future Sight (107), Aptitude (108), Locktouch (112), Paragon (138), Ballistician skills (149->152) and Warp (154)

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
            if skills[0] == 3 and 'Str' in self.readClassAttackType(className):
                skills[0] = 2
            if skills[0] == 2 and 'Mag' in self.readClassAttackType(className):
                skills[0] = 3

            # Def/Res +2
            if skills[0] == 8 and self.readClassDefenseType(className) == 'Def':
                skills[0] = 7
            if skills[0] == 7 and self.readClassDefenseType(className) == 'Res':
                skills[0] = 8

            # Malefic Aura
            if skills[0] == 76 and not className in self.TOME_CLASSES:
                while skills[0] == 76:
                    skills[0] = self.rng.choice(allBaseSkills2)

            # Shadowgift
            if skills[0] == 141 and not className in self.TOME_CLASSES:
                while skills[0] == 141:
                    skills[0] = self.rng.choice(allBaseSkills1)

            # Live to Serve
            if skills[2] == 100 and not (className == 'Hoshido Noble' or className in self.FELICIA_CLASSES or className in self.JAKOB_CLASSES):
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
                        if className not in ["Wyvern Lord", "Blacksmith", "Hero", "Maid", "Butler", "Sorcerer", "Bow Knight", "Vanguard", "Dread Fighter", "Master of Arms", "Oni Chieftain", "Basara"]:
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
        characterNames = self.PMU_CHARACTERS.copy()
        PMUList = ['Corrin', 'Azura']
        characterNames.remove('Azura')
        if self.rng.random() < 0.5:
            PMUList.append('Jakob')
        else:
            PMUList.append('Felicia')
        characterNames.remove('Jakob')
        characterNames.remove('Felicia')
        if self.gameRoute == 'Conquest':
            PMUList.append(self.earlyConquestRecruit)
            characterNames.remove(self.earlyConquestRecruit)
        else:
            PMUList.append(self.earlyBirthrightRecruit)
            characterNames.remove(self.earlyBirthrightRecruit)
        n = len(characterNames) + 1
        benford = np.log(1+1/np.arange(1,n)) / np.log(n)
        PMUList = PMUList + self.rng.choice(characterNames, 12, replace=False, p=benford).tolist()
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

    def setCharacterPromotionLevel(self, character, level):
        character['LevelData']['@internalLevel'] = str(level)
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

        className = characterData['NewBaseClass']
        classDefenseType = self.readClassDefenseType(className)
        i, j = 6, 7  # default: 'Def'
        if classDefenseType == 'Res':
            i, j = 7, 6
        elif classDefenseType == 'Mixed':
            if self.rng.random() < self.defResRatio:  # Def is supposed to be more common
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

    def adjustCharacterStrMag(self, characterData):
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
        if 'Mixed' in classAttackType or (classAttackType == 'Str' and self.rng.random() < self.strMixedAttackerP):
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

        else:  # pure Str or Mag attacker
            probas = self.addmax(np.ones(8))
            probas2 = self.addmax(np.ones(8))
            probas[j] = 0
            probas2[j] = 0
            probas = self.addmax(probas)
            probas2 = self.addmax(probas2)

            while stats[j] > 0:
                s = self.rng.choice(8, p=probas)
                if stats[s] < self.baseStatCap:
                    stats[j] -= 1
                    stats[s] += 1
                else:
                    probas[s] = 0
                    probas = self.addmax(probas)

            while growths[j] > 0:
                s = self.rng.choice(8, p=probas2)
                if growths[s] < self.growthCap:
                    growths[j] -= 5
                    growths[s] += 5
                else:
                    probas2[s] = 0
                    probas2 = self.addmax(probas2)

        if self.rng.random() < self.swapStrMagP:
            growths[i], growths[j] = growths[j], growths[i]
            stats[i], stats[j] = stats[j], stats[i]
            modifiers[i], modifiers[j] = modifiers[j], modifiers[i]

        return characterData

    def swapRetainerStats(self, characterData):
        """
        Nerfs the retainers' relevant offensive stat: puts it at 3rd rank for base stats
        """
        className = characterData['NewClass']
        classAttackType = self.readClassAttackType(className)
        stats = characterData['BaseStats']

        if classAttackType in ['Str', 'StrMixed']:
            i = 1  # Str
            j = np.argsort(stats)[-4] # 4th highest base stat
            if stats[i] > stats[j]:
                stats[i], stats[j] = stats[j], stats[i]
        else:
            i = 2  # Mag
            j = np.argsort(stats)[-4] # 4th highest base stat
            if stats[i] > stats[j]:
                stats[i], stats[j] = stats[j], stats[i]

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
            with open('{}/PMUClassSpread.csv'.format(path), 'w') as fcsv:
                writer = csv.writer(fcsv, delimiter='\t')
                for name in [x for x in ['Corrin'] + self.ROUTE_CHARACTERS if x in self.PMUList]:
                    className = self.randomizedClasses[name]
                    row = [name, className]
                    if not self.disableModelSwitch:
                        row.insert(1, self.readSwitchedCharacterName(name))
                    if self.enableRandomizedPersonalSkills:
                        personalSkill = self.personalSkills[name]
                        row.append(personalSkill)
                    writer.writerow(row)
            with open('{}/ClassSpread.csv'.format(path), 'w') as fcsv:
                writer = csv.writer(fcsv, delimiter='\t')
                for name in [x for x in ['Corrin'] + self.ROUTE_CHARACTERS if x in self.randomizedClasses.keys()]:
                    className = self.randomizedClasses[name]
                    row = [name, className]
                    if not self.disableModelSwitch:
                        row.insert(1, self.readSwitchedCharacterName(name))
                    if self.enableRandomizedPersonalSkills:
                        personalSkill = self.personalSkills[name]
                        row.append(personalSkill)
                    writer.writerow(row)

        for character in self.settings['root']['Character']:
            switchingcharacterName = self.readSwitchingCharacterName(character)
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
        adjustStrategyCoeff=args.adjust_strategy_coeff,
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
        debuffPrepromotesCoeff=args.debuff_prepromotes_coeff,
        defResRatio=args.def_res_ratio,
        disableBalancedSkillRandomization=args.disable_balanced_skill_randomization,
        disableModelSwitch=args.disable_model_switch,
        enableDLCBaseClass=args.enable_dlc_base_class,
        enableGenderlessDLC=args.enable_genderless_dlc,
        enableRandomizedPersonalSkills=args.enable_randomized_personal_skills,
        fatesUpgraded=(not args.disable_fates_upgraded),
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
        imposedClasses=args.imposed_classes,
        limitStaffClasses=(not args.disable_limit_staff_classes),
        modifierCoefficient=args.modifier_coefficient,
        modP=args.mod_p,
        nPasses=args.n_passes,
        nSkills=args.n_skills,
        PMUMode=args.pmu_mode,
        randomizeStatsAndGrowthsSum=(not args.disable_randomize_stats_growths_sum),
        rebalanceLevels=(not args.disable_rebalance_levels),
        rngLevelupP=args.rng_levelup_p,
        seed=args.seed,
        statP=args.stat_p,
        strMixedAttackerP=args.str_mixed_attacker_p,
        swapAtkDefP=args.swap_atk_def_p,
        swapDefResP=args.swap_def_res_p,
        swapLckP=args.swap_lck_p,
        swapSklSpdP=args.swap_skl_spd_p,
        swapStrMagP=args.swap_str_mag_p,
        verbose=args.verbose
    )

    fatesRandomizer.run()
