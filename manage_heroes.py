import extract_data, traceback
from unidecode import unidecode

# region Raw Data Variables
translations = extract_data.getTranslations()
resplendent_hero_list = extract_data.getResplendentData() # returns list of hero pid who are resplendents
# endregion

hero_id_nums = {}
hero_id_to_name = {}
def individualHeroData(hero):
    try:
        hero_name = translations['M'+hero['id_tag']]
        if "_F_" in hero['roman'] or hero['roman'][-2:] == "_F" or hero['roman'] == "BELETH":
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

        if hero_name == "Byleth":
            hero_name = "Byleth_F"

        if unidecode(hero_name) != hero_name:
            hero_name = unidecode(hero_name) # fixes issues with names like Hríd, Líf and Gunnthrá by removing the accents

        if not hero_name in hero_id_nums.keys():
            hero_id_nums[hero_name] = [{'id': hero['id_tag'], 'id_num': hero['id_num']}]
        else:
            for i in range(len(hero_id_nums[hero_name])):
                if hero_id_nums[hero_name][i]['id_num'] > hero['id_num']:
                    hero_id_nums[hero_name].insert(i, {'id': hero['id_tag'], 'id_num': hero['id_num']})
                    break
                elif i == len(hero_id_nums[hero_name]) - 1:
                    hero_id_nums[hero_name].append({'id': hero['id_tag'], 'id_num': hero['id_num']})

        hero_id_to_name[hero['id_tag']] = hero_name

        # Skill Management
        skills = [[], [], [], [], []]
        for i, tier in enumerate(hero['skills']):
            for j, sid in enumerate(tier):
                # print(sid)
                if sid != None:
                    skills[i].append(sid)
        

        return {
            'name': translations['M'+hero['id_tag']],
            'title': translations['M'+hero['id_tag'].replace('_','_HONOR_',1)],
            'id': hero['id_tag'],
            'image': '',
            'max_dragonflowers': hero['dragonflowers']['max_count'],
            'base_stats': hero['base_stats'],
            'growth_rates': hero['growth_rates'],
            'blessing_bonus': extract_data.getBlessingBonus(hero),
            'blessing': extract_data.getBlessing(hero),
            'resplendent': hero['id_tag'] in resplendent_hero_list,
            'movement_type': hero['move_type'],
            'unit_type': hero['weapon_type'],
            'skills': skills,
            'game': extract_data.removeMaskRaw(hero['origins'], len(extract_data.origins)),
            'refresher': hero['refresher']
        }
    except KeyError:
        pass

def generateHeroList(raw_hero_list):
    updatedHeroList = []
    for hero in raw_hero_list:
        data = individualHeroData(hero)
        if data:
            updatedHeroList.append(data)
    
    for hero in updatedHeroList:
        hero_name = hero_id_to_name[hero['id']]
        for i in range(len(hero_id_nums[hero_name])):
            if hero_id_nums[hero_name][i]['id'] == hero['id']:
                hero_name += "_" + str(i + 1)
                hero['image'] = hero_name.lower()
                break
    return updatedHeroList

def generateHeroDict(hero_list):
    hero_dict = {}
    for hero in hero_list:
        hero_dict[hero['id']] = hero
    return hero_dict

def heroListfromHeroDict(hero_dict):
    return list(hero_dict.values())
# hero_name = id_translations['M'+hero['id_tag']]
#             actual_name = hero_name
#             hero_title = id_translations['M'+hero['id_tag'].replace('_','_HONOR_',1)]

#             hero_type = ""
#             hero_rarity = ""
#             # Male and Female can be seperated here by getting finding if there is _M_ or _F_ in the roman name
#             # The base forms don't have the second dash so much be found by splicing the end of the string
#             # Splicing has to be done to avoid potential errors (e.g. _F in roman name would also get caught on "FESTIVAL" or similar

#             if "_F_" in hero['roman'] or hero['roman'][-2:] == "_F" or hero['roman'] == "BELETH":
#                 if "ECHIDNA" in hero['roman']:
#                     print(hero)
#                 if "Marth" in hero_name:
#                     hero_name = "Marth_Masked"
#                 else:
#                     hero_name = hero_name + "_F"
#             elif "_M_" in hero['roman'] or hero['roman'][-2:] == "_M"  or hero['roman'] == "BYLETH":
#                 hero_name = hero_name + "_M"
#             elif "_A_" in hero['roman'] or hero['roman'][-2:] == "_A": # Tiki (Adult)
#                 hero_name = hero_name + "_A"
#             elif "TIKI" in hero['roman']: # Tiki (Young)
#                 hero_name = hero_name + "_Y"

#             if unidecode(hero_name) != hero_name:
#                 hero_name = unidecode(hero_name) # fixes issues with names like Hríd, Líf and Gunnthrá by removing the accents

#             # id_tag
#             if not hero_name in hero_storage.keys():
#                 hero_storage[hero_name] = []
#                 hero_id_nums[hero_name] = []