import os, shutil, sys, json, traceback, math, difflib
from unidecode import unidecode

#region GLOBALS
categories = ['weapon', 'assist', 'special', 'a', 'b', 'c', 's', 'Refine Weapon Skill Effect', 'Beast Transformation Effect']
weapons = ['sword', 'lance', 'axe', 'red_bow', 'blue_bow', 'green_bow', 'colorless_bow', 'red_dagger', 'blue_dagger', 'green_dagger', 'colorless_dagger', 'red_tome', 'blue_tome', 'green_tome', 'colorless_tome', 'staff', 'red_breath', 'blue_breath', 'green_breath', 'colorless_breath', 'red_beast', 'blue_beast', 'green_beast', 'colorless_beast']
movement_type = ['infantry', 'armor', 'cavalry', 'flying']
origins = ['heroes', 'shadow_dragon_new_mystery', 'echoes', 'genealogy', 'thracia', 'binding', 'blazing', 'sacred', 'path', 'dawn', 'awakening', 'fates', 'houses', 'mirage']
blessings = [None, 'fire', 'water', 'wind', 'earth', 'light', 'dark', 'astra', 'anima']

def removeMask(mask, raw):
    ret = []
    for i in range(len(raw)):
        if mask & 2**i:
            ret.append(raw[i])
    return ret

def removeMaskRaw(mask, length):
    ret = []
    for i in range(length):
        if mask & 2**i:
            ret.append(i)
    return ret

def getBlessing(hero):
    blessing = 0
    if hero['legendary']:
        blessing = hero['legendary']['element']
    return blessing

def getBlessingBonus(hero):
    blessingBonus = {'hp': 0, 'atk': 0, 'def': 0, 'spd': 0, 'res': 0}
    if hero['legendary']:
        blessingBonus = hero['legendary']['bonus_effect']
    return blessingBonus

def generateSkillData(skill):
    name = id_translations[skill['name_id']]
    description = id_translations[skill['desc_id']]
    skill_id = name.lower().replace(' ', '_').replace('.','').replace('/','_').replace("'",'') # "ID" of skill
    image = skill_id
    if skill['category'] == 0:
        image = "generic_weapon"
    elif skill['category'] == 1:
        image = "generic_assist"
    elif skill['category'] == 2:
        image = "generic_special"

    inheritable_weapons = removeMaskRaw(skill['wep_equip'], len(weapons))
    inheritable_movement = removeMaskRaw(skill['mov_equip'], len(movement_type))

    return {
        'name': name,
        'description': description,
        'type': categories[skill['category']],
        'image': image,
        'inheritable': not skill['exclusive'],
        'refined': False,
        'might': skill['might'],
        'id': skill_id,
        'restrictedTo': {'moveType': inheritable_movement, 'weaponType': inheritable_weapons},
        'sp': skill['sp_cost'],
        'stats': skill['stats'],
        'score': skill['score'],
        'cooldown': skill['cooldown_count'],
        'fodder': [[], [], [], [], []]
    }

def generateSkillDataWithFodder(skill):
    name = id_translations[skill['name_id']]
    description = id_translations[skill['desc_id']]
    skill_id = name.lower().replace(' ', '_').replace('.','').replace('/','_').replace("'",'') # "ID" of skill
    image = skill_id
    if skill['category'] == 0:
        image = "generic_weapon"
    elif skill['category'] == 1:
        image = "generic_assist"
    elif skill['category'] == 2:
        image = "generic_special"

    inheritable_weapons = removeMaskRaw(skill['wep_equip'], len(weapons))
    inheritable_movement = removeMaskRaw(skill['mov_equip'], len(movement_type))
    return {
        'name': name,
        'description': description,
        'type': categories[skill['category']],
        'image': image,
        'inheritable': not skill['exclusive'],
        'id': skill_id,
        'refined': False,
        'might': skill['might'],
        'restrictedTo': {'moveType': inheritable_movement, 'weaponType': inheritable_weapons},
        'sp': skill['sp_cost'],
        'score': skill['score'],
        'stats': skill['stats'],
        'cooldown': skill['cooldown_count'],
        'fodder': skills_dict[skill_id]['fodder']
    }

def generateRefineSkillData(skill):
    try:
        name = id_translations[skill['name_id']]
        description = id_translations[skill['desc_id']]
        if description == None:
            description = ''

        inheritable_weapons = removeMaskRaw(skill['wep_equip'], len(weapons))
        inheritable_movement = removeMaskRaw(skill['mov_equip'], len(movement_type))

        image = 'none'

        skill_id = name.lower().replace(' ', '_').replace('.','').replace('/','_').replace("'",'') # "ID" of skill
        
        if skill['refine_sort_id'] == 1:
            if inheritable_weapons[0] == 15:
                image = 'wrathful_staff_eff'
                skill_id += "_wrathful"
                name += " (Wrathful)"
            else:
                image = skill_id + '_eff'
                skill_id += "_eff"
                name += " (Eff)"
        elif skill['refine_sort_id'] == 2:
            image = 'dazzling_staff_eff'
            skill_id += "_dazzling"
            name += " (Dazzling)"
        elif skill['refine_sort_id'] == 101:
            image = 'refine_atk'
            skill_id += "_atk"
            name += " (+Mt)"
        elif skill['refine_sort_id'] == 102:
            image = 'refine_spd'
            skill_id += "_spd"
            name += " (+Spd)"
        elif skill['refine_sort_id'] == 103:
            image = 'refine_def'
            skill_id += "_def"
            name += " (+Def)"
        elif skill['refine_sort_id'] == 104:
            image = 'refine_res'
            skill_id += "_res"
            name += " (+Res)"


        if skill['refine_sort_id'] in [1,2]:
            index_id = 'M' + skill['refine_id'].replace('_', '_H_', 1)
            description += ' ' + id_translations[index_id]
            if skill['refine_stats']['hp'] > 0:
                description += ' +{} HP.'.format(skill['refine_stats']['hp'])
        elif skill['refine_stats']['hp'] > 0:
            append_string = ' +{} HP '.format(skill['refine_stats']['hp'])
            for key, value in skill['refine_stats'].items():
                if value > 0 and key != 'hp':
                    append_string += ' +{} {}.'.format(value, key.capitalize())
            description += append_string
        return {
            'name': name,
            'description': description,
            'type': categories[skill['category']],
            'image': image,
            'id': skill_id,
            'inheritable': not skill['exclusive'],
            'refined': skill['refined'],
            'might': skill['might'],
            'restrictedTo': {'moveType': inheritable_movement, 'weaponType': inheritable_weapons},
            'sp': skill['sp_cost'],
            'score': skill['score'],
            'cooldown': 0,
            'stats': skill['stats']
        }
    except KeyError:
        # traceback.print_exc()
        pass
    except Exception:
        traceback.print_exc()
        pass
#endregion

id_translations = {}
def getTranslations():
    for filename in os.listdir('./files/assets/Common/SRPG/Skill'):
        try:
            with open('./files/assets/USEN/Message/Data/Data_'+filename, encoding='utf8') as json_file:
                data = json.load(json_file)
                for point in data:
                    id_translations[point['key']] = point['value']
        except Exception:
            traceback.print_exc()
            pass

raw_skill_list = []
def getRawSkills():
    for filename in os.listdir('./files/assets/Common/SRPG/Skill'):
        try:
            with open('./files/assets/Common/SRPG/Skill/'+filename, encoding='utf8') as json_file:
                data = json.load(json_file)
                for point in data:
                    if point['enemy_only'] == False:
                        raw_skill_list.append(point)
        except Exception:
            traceback.print_exc()
            pass

raw_hero_list = []
def getRawHeroes():
    for filename in os.listdir('./files/assets/Common/SRPG/Person'):
        try:
            with open('./files/assets/Common/SRPG/Person/'+filename, encoding='utf8') as json_file:
                data = json.load(json_file)
                for point in data:
                    raw_hero_list.append(point)
        except Exception:
            traceback.print_exc()
            pass
grail_heroes = [["Darros", "Seawalker"], ["Lorenz", "Highborn Heat"], ["Eremiya", "Bishop of Woe"], ["Jorge", "Traveling Peddler"]]
def getGrailHeroes():
    for filename in os.listdir('./files/assets/Common/HolyGrail'):
        try:
            with open('./files/assets/Common/HolyGrail/'+filename, encoding='utf8') as json_file:
                data = json.load(json_file)
                for point in data:
                    hero_id = point['reward'][0]['id_tag']
                    hero_name = id_translations['M' + hero_id]
                    hero_title = id_translations['M'+hero_id.replace('_','_HONOR_',1)]
                    if not [hero_name, hero_title] in grail_heroes:
                        grail_heroes.append([hero_name, hero_title])
        except Exception:
            traceback.print_exc()
            pass

resplendent_hero_ids = []
def getResplendentData():
    for filename in os.listdir('./files/assets/Common/SubscriptionCostume'):
        try:
            with open('./files/assets/Common/SubscriptionCostume/'+filename, encoding='utf8') as json_file:
                data = json.load(json_file)
                for point in data:
                    resplendent_hero_ids.append(point['hero_id'])
        except Exception:
            traceback.print_exc()
            pass

seal_sid = []
def getSealData(): # Gets seal and if is max tier
    for filename in os.listdir('./files/assets/Common/SRPG/SkillAccessory'):
            with open('./files/assets/Common/SRPG/SkillAccessory/'+filename, encoding='utf-8') as json_file:
                seal_data = json.load(json_file)
                for data in seal_data:
                    try:
                        seal_sid.append(['M'+data['id_tag'], data['next_seal'] == None])
                    except:
                        pass

max_tier_skills_by_category = [[], [], [], [], [], [], [], [], []]
def getMaxTierSkills():
    for skill in raw_skill_list:
        try:
            if not skill['next_skill']:
                skill_data = generateSkillDataWithFodder(skill)
                if [skill['name_id'], True] in seal_sid:
                    max_tier_skills_by_category[6].append(skill_data)
                
                if skill['category'] != 6 and not (skill['category'] == 0 and skill['refine_sort_id'] > 0):
                    max_tier_skills_by_category[skill['category']].append(skill_data)
        except KeyError:
            pass
        except Exception:
            traceback.print_exc()
            pass

skills_dict = {}
def getSkillsDict():
    for skill in raw_skill_list:
        try:
            skill_data = generateSkillData(skill)
            name = id_translations[skill['name_id']]
            skill_id = name.lower().replace(' ', '_').replace('.','').replace('/','_').replace("'",'') # "ID" of skill
            skills_dict[skill_id] = skill_data
        except KeyError:
            # traceback.print_exc()
            pass
        except Exception:
            traceback.print_exc()
            pass

old_hero_data = {}
def getOldHeroData():
    global old_hero_data
    with open('OLD_DATA.json', 'r') as json_file:
        old_hero_data = json.load(json_file)

refine_skill_data = {}
def manageRefines():
    for skill in raw_skill_list:
        try:
            #? 0 = no refine/base weapons
            #? 1 = eff refine, wrathful for staves
            #? 2 = dazzling refine for staves
            #? 101-104 = atk/spd/def/res refinements in that order
            if categories[skill['category']] == 'weapon' and skill['refine_sort_id'] != 0:
                skill_data = generateRefineSkillData(skill)
                if skill_data == None:
                    print(skill)
                name = id_translations[skill['name_id']]
                skill_id = name.lower().replace(' ', '_').replace('.','').replace('/','_').replace("'",'') # "ID" of skill
                if not skill_id in refine_skill_data.keys():
                    refine_skill_data[skill_id] = []
                refine_skill_data[skill_id].append(skill_data)
                skills_dict[skill_data['id']] = skill_data
        except KeyError:
            traceback.print_exc()
            pass
        except Exception:
            traceback.print_exc()
            pass

def addSkills(hero):
    try:
        skills = hero['skills']
        hero_skill_list = [[], [], [], [], []]
        for i in range(len(skills)):
            for j in range(len(skills[i])):
                skill = skills[i][j]
                if skill != None:
                    skill_id = id_translations['M' + skill].lower().replace(' ', '_').replace('.','').replace('/','_').replace("'",'') # "ID" of skill
                    hero_skill_list[i].append(skill_id)
                    skills_dict[skill_id]['fodder'][i].append(hero['id'])
        return hero_skill_list
    except KeyError:
        # traceback.print_exc()
        pass
    except Exception:
        traceback.print_exc()
        pass

hero_list = []
hero_dict = {}

hero_id_nums = {}
def formatHeroes():
    print("WARNING: Seasonals defaults to 5 stars")
    hero_storage = {}
    for hero in raw_hero_list:
        try:
            hero_name = id_translations['M'+hero['id_tag']]
            actual_name = hero_name
            hero_title = id_translations['M'+hero['id_tag'].replace('_','_HONOR_',1)]

            hero_type = ""
            hero_rarity = ""
            # Male and Female can be seperated here by getting finding if there is _M_ or _F_ in the roman name
            # The base forms don't have the second dash so much be found by splicing the end of the string
            # Splicing has to be done to avoid potential errors (e.g. _F in roman name would also get caught on "FESTIVAL" or similar)
            if hero['permanent_hero'] == True:
                hero_type = "permanent" # Alfonse, Sharena and Anna
                hero_rarity = "none"
            elif [hero_name, hero_title] in grail_heroes:
                hero_type = "grail"
                hero_rarity = "none"
            elif hero['regular_hero'] == False:
                if hero['legendary'] == None:
                    if "POPULARITY" in hero['roman']:
                        hero_type = "regular" # CYL Units
                        hero_rarity = "five_star"
                    elif "Normal" in hero['face_name']:
                        hero_type = "regular" # Farfetched heroes, refreshers
                    else:
                        hero_type = "seasonal"
                        hero_rarity = "five_star"
                else:
                    if hero['legendary']['kind'] == 1:
                        if hero['legendary']['element'] < 5:
                            hero_type = "legendary"
                            hero_rarity = "five_star"
                        else:
                            hero_type = "mythic"
                            hero_rarity = "five_star"
                    else:
                        if hero['legendary']['kind'] == 2:
                            hero_type = "duo"
                            hero_rarity = "five_star"
                        else:
                            hero_type = "resonant"
                            hero_rarity = "five_star"
            else:
                hero_type = "regular"

            if "_F_" in hero['roman'] or hero['roman'][-2:] == "_F" or hero['roman'] == "BELETH":
                if "ECHIDNA" in hero['roman']:
                    print(hero)
                if "Marth" in hero_name:
                    hero_name = "Marth_Masked"
                else:
                    hero_name = hero_name + "_F"
            elif "_M_" in hero['roman'] or hero['roman'][-2:] == "_M"  or hero['roman'] == "BYLETH":
                hero_name = hero_name + "_M"
            elif "_A_" in hero['roman'] or hero['roman'][-2:] == "_A": # Tiki (Adult)
                hero_name = hero_name + "_A"
            elif "TIKI" in hero['roman']: # Tiki (Young)
                hero_name = hero_name + "_Y"

            if unidecode(hero_name) != hero_name:
                hero_name = unidecode(hero_name) # fixes issues with names like Hríd, Líf and Gunnthrá by removing the accents

            # id_tag
            if not hero_name in hero_storage.keys():
                hero_storage[hero_name] = []
                hero_id_nums[hero_name] = []
            hero_data = {
                'name': actual_name,
                'title': hero_title,
                'id': 'REPLACE',
                'max_dragonflowers': hero['dragonflowers']['max_count'],
                'base_stats': hero['base_stats'],
                'growth_rates': hero['growth_rates'],
                'blessing_bonus': getBlessingBonus(hero),
                'blessing': getBlessing(hero),
                'resplendent': hero['id_tag'] in resplendent_hero_ids,
                'movement_type': hero['move_type'],
                'unit_type': hero['weapon_type'],
                'rarity': hero_rarity,
                'availability': hero_type,
                'skills': hero['skills'],
                'game': removeMaskRaw(hero['origins'], len(origins)),
                'refresher': hero['refresher']
            }

            for i, hero_i in enumerate(hero_storage[hero_name]):
                if hero['id_num'] < hero_id_nums[hero_name][i]:
                    hero_storage[hero_name].insert(i, hero_data)
                    hero_id_nums[hero_name].insert(i, hero['id_num'])
                    break
            else:
                hero_storage[hero_name].insert(len(hero_storage[hero_name]), hero_data)
                hero_id_nums[hero_name].insert(len(hero_storage[hero_name]), hero['id_num'])
        except KeyError:
            # traceback.print_exc()
            # print(hero['id_num'], hero_i)
            pass
        except Exception:
            traceback.print_exc()
            pass
    
    for hero_index, hero_group in hero_storage.items():
        for i, hero in enumerate(hero_group):
            hero_id = hero_index.lower() + "_" + str(i + 1)
            if hero_id == "byleth_1":
                hero_id = "byleth_f_2" # Duo Hero Exception
            hero['id'] = hero_id
            hero['skills'] = addSkills(hero)
            if hero['rarity'] == "":
                if hero['id'] in old_hero_data.keys():
                    rarity = old_hero_data[hero['id']]['rarity']
                    if rarity == "REPLACE":
                        print("WARNING: Hero Rarity could not be found - this will need to be manually entered for hero {}: {}".format(hero_id, hero['title']))
                        id = input("What is their rarity ('four' or 'five')")
                        if id == "four":
                            id = "three_star_four_star"
                        elif id == "five":
                            id = "five_star"
                            
                        hero['rarity'] = rarity
                    else:
                        hero['rarity'] = rarity
                else:
                    print("WARNING: Hero Rarity could not be found - hero ID does not exist in old hero data!\nIf this is a new hero, you will need to manually enter this data for hero {}: {}".format(hero_id, hero['title']))
                    id = input("What is their rarity ('four' or 'five')")
                    if id == "four":
                        id = "three_star_four_star"
                    elif id == "five":
                        id = "five_star"
                        
                    hero['rarity'] = rarity
            #TODO: availability could potentially be gathered from a combination of 'legendary' to get duo, resonant, legendary and mythic as well as regular_hero to get regular pool
            #TODO: This causes issues because its impossible to determine the exact origin of the hero without banner data. Actually it might be if you use some advanced 5head shit
            #TODO: but idk
            #TODO: Potentially just merge this with old data to fix the ones that do have problems (e.g. surtr). Seperating GHB and TT+ units might be hard though
            #TODO: Actually i can separate those by finding what GHB units i can get from the GHB maps (see test.py) vs what units are available in the grail shop
            #TODO: one's in grail shop that aren't available from GHB are obviously TT+ units
            #TODO: that doesn't fix newer TT+ units e.g. darros, etc. but those can be fixed by looking in the recent arena cycles
            #TODO: that causes an issue when a seasonal unit is in the slot where the TT+ unit usually is, however, but IDK
            hero_list.append(hero)
            hero_dict[hero_id] = hero



# Managing Raw Data
getTranslations()
getRawSkills()
getRawHeroes()
getGrailHeroes()
getOldHeroData()
getResplendentData()
getSealData()

# Manipulating the Data
getSkillsDict()
getMaxTierSkills()
manageRefines()
formatHeroes()

# Exporting Data
def exportData():
    if len(max_tier_skills_by_category) > 0:
        with open('max_tier_skills_by_category.json', 'w') as outfile:
            json.dump(max_tier_skills_by_category, outfile)
    
    if len(refine_skill_data) > 0:
        with open('refine_skill_data.json', 'w') as outfile:
            json.dump(refine_skill_data, outfile)
# as outfile:
#             json.dump(hero_list, outfile)
        
        # with open('heroes_by_id.json', 'w') as outfile:
        #     json.dump(hero_dict, outfile)
    
    if len(skills_dict.keys()) > 0:
        with open('skills_dict.json', 'w') as outfile:
            json.dump(skills_dict, outfile)
    
    if len(hero_dict.keys()) > 0:
        with open('hero_dict.json', 'w') as outfile:
            json.dump(hero_dict, outfile)
        
        with open('hero_list.json', 'w') as outfile:
            json.dump(hero_list, outfile)
    
    with open('key_values.json', 'w', encoding='utf8') as outfile:
        json.dump(id_translations, outfile, ensure_ascii=False)
exportData()
