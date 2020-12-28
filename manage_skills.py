import extract_data, traceback
from unidecode import unidecode

# region Raw Data Variables
translations = extract_data.getTranslations()
#endregion

def findFodder(skill, hero_list):
    fodder = [[], [], [], [], []]
    for hero in hero_list:
        for i, tier in enumerate(hero['skills']):
            for sid in tier:
                if sid == skill['id_tag']:
                    fodder[i].append(hero['id'])
    return fodder

skill_name_counts = {}
def generateSkillData(skill, hero_list):
    name = translations[skill['name_id']]
    if not name in skill_name_counts.keys() and not skill['refined']:
        skill_name_counts[name] = []
    
    description = translations[skill['desc_id']]
    skill_id = name.lower().replace(' ', '_').replace('.','').replace('/','_').replace("'",'') # "ID" of skill

    if not skill['refined'] and skill['category'] == 0:
        if not skill['id_tag'] in skill_name_counts[name]:
            skill_name_counts[name].append(skill['id_tag'])
        index = 1
        for i in range(len(skill_name_counts[name])):
            if skill_name_counts[name][i] == skill['id_tag']:
                index = i + 1
        skill_id += "_" + str(index)

    image = skill_id
    if skill['category'] == 0:
        image = "generic_weapon"
    elif skill['category'] == 1:
        image = "generic_assist"
    elif skill['category'] == 2:
        image = "generic_special"

    inheritable_weapons = extract_data.removeMaskRaw(skill['wep_equip'], len(extract_data.weapons))
    inheritable_movement = extract_data.removeMaskRaw(skill['mov_equip'], len(extract_data.movement_type))

    fodder = findFodder(skill, hero_list)
    return{
        'name': name,
        'description': description,
        'type': extract_data.categories[skill['category']],
        'image': image,
        'inheritable': not skill['exclusive'],
        'refined': skill['refined'],
        'might': skill['might'],
        'id': skill['id_tag'],
        'restrictedTo': {'moveType': inheritable_movement, 'weaponType': inheritable_weapons},
        'sp': skill['sp_cost'],
        'stats': skill['stats'],
        'score': skill['score'],
        'cooldown': skill['cooldown_count'],
        'fodder': fodder
    }

def generateRefineSkillData(skill, hero_list):
    skill_data = generateSkillData(skill, hero_list)
    image = 'none'
    name = skill_data['name']
    index = 1
    if name in skill_name_counts.keys():
        for i in range(len(skill_name_counts[name])):
            if skill_name_counts[name][i] == skill['refine_base']:
                index = i + 1
                break
        if skill['refine_base'] not in skill_name_counts[name]:
            skill_name_counts[name].append(skill['refine_base'])
            index = len(skill_name_counts[name])
    else:
        skill_name_counts[name] = [skill['refine_base']]

    skill_id = name.lower().replace(' ', '_').replace('.','').replace('/','_').replace("'",'') # "ID" of skill

    if index > 1:
        skill_id += "_" + str(index) # adds number if index > 1

    skill_id = unidecode(skill_id) # removes special characters
    
    if skill['refine_sort_id'] == 1:
        if skill_data['restrictedTo']['weaponType'][0] == 15:
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

    skill_data['base'] = skill['refine_base']
    skill_data['name'] = name
    skill_data['image'] = image
    return skill_data

def generateSkillList(raw_skill_list, hero_list):
    skill_list = []
    for skill in raw_skill_list:
        try:
            if skill['refined']:
                skill_list.append(generateRefineSkillData(skill, hero_list))
            else:
                skill_list.append(generateSkillData(skill, hero_list))
        except:
            # traceback.print_exc()
            pass
    return skill_list

def generateSkillDict(skill_list):
    skill_dict = {}
    for skill in skill_list:
        skill_dict[skill['id']] = skill
    return skill_dict

def getMaxTierSkills(raw_skill_list, hero_list, seal_sid):
    max_tier_skills_by_category = [[], [], [], [], [], [], [], [], []]
    for skill in raw_skill_list:
        try:
            if not skill['next_skill']:
                skill_data = generateSkillData(skill, hero_list)
                if [skill['name_id'], True] in seal_sid:
                    max_tier_skills_by_category[6].append(skill_data)
                
                if skill['category'] != 6 and not (skill['category'] == 0 and skill['refine_sort_id'] > 0):
                    max_tier_skills_by_category[skill['category']].append(skill_data)
        except KeyError:
            pass
        except Exception:
            # Duo Skill / Beast Skill
            pass
    return max_tier_skills_by_category

def getRefineSkills(skill_dict, refine_dictionary, hero_dict):
    new_refine_dict = {}
    for key, value in refine_dictionary.items():
        refines = []
        for i in range(len(value)):
            refine_id = value[i]
            try:
                if skill_dict[refine_id]['refined'] == False:
                    for fodder_tier in skill_dict[key]['fodder']:
                        for unit_id in fodder_tier:
                            hero_dict[unit_id]['skills'][4].append(skill_dict[refine_id]['id'])
                            skill_dict[refine_id]['fodder'][4].append(unit_id)
                            # refine_dictionary.remove(refine_id)
            except KeyError:
                # print(skill_dict)
                raise
            else:
                refines.append(skill_dict[refine_id])
        if len(refines) > 0:
            new_refine_dict[key] = refines
    
    return hero_dict, new_refine_dict, skill_dict

def skillListFromSkillDict(skill_dict):
    return list(skill_dict.values())

# def updateHeroListAndGetRefines(hero_list, refine_data):

# def generateRefineSkillData(skill):
#     try:
#         name = id_translations[skill['name_id']]
#         description = id_translations[skill['desc_id']]
#         if description == None:
#             description = ''

#         inheritable_weapons = removeMaskRaw(skill['wep_equip'], len(weapons))
#         inheritable_movement = removeMaskRaw(skill['mov_equip'], len(movement_type))

#         image = 'none'

#         skill_id = name.lower().replace(' ', '_').replace('.','').replace('/','_').replace("'",'') # "ID" of skill
        
#         if skill['refine_sort_id'] == 1:
#             if inheritable_weapons[0] == 15:
#                 image = 'wrathful_staff_eff'
#                 skill_id += "_wrathful"
#                 name += " (Wrathful)"
#             else:
#                 image = skill_id + '_eff'
#                 skill_id += "_eff"
#                 name += " (Eff)"
#         elif skill['refine_sort_id'] == 2:
#             image = 'dazzling_staff_eff'
#             skill_id += "_dazzling"
#             name += " (Dazzling)"
#         elif skill['refine_sort_id'] == 101:
#             image = 'refine_atk'
#             skill_id += "_atk"
#             name += " (+Mt)"
#         elif skill['refine_sort_id'] == 102:
#             image = 'refine_spd'
#             skill_id += "_spd"
#             name += " (+Spd)"
#         elif skill['refine_sort_id'] == 103:
#             image = 'refine_def'
#             skill_id += "_def"
#             name += " (+Def)"
#         elif skill['refine_sort_id'] == 104:
#             image = 'refine_res'
#             skill_id += "_res"
#             name += " (+Res)"


#         if skill['refine_sort_id'] in [1,2]:
#             index_id = 'M' + skill['refine_id'].replace('_', '_H_', 1)
#             description += ' ' + id_translations[index_id]
#             if skill['refine_stats']['hp'] > 0:
#                 description += ' +{} HP.'.format(skill['refine_stats']['hp'])
#         elif skill['refine_stats']['hp'] > 0:
#             append_string = ' +{} HP '.format(skill['refine_stats']['hp'])
#             for key, value in skill['refine_stats'].items():
#                 if value > 0 and key != 'hp':
#                     append_string += ' +{} {}.'.format(value, key.capitalize())
#             description += append_string
#         return {
#             'name': name,
#             'description': description,
#             'type': categories[skill['category']],
#             'image': image,
#             'id': skill_id,
#             'inheritable': not skill['exclusive'],
#             'refined': skill['refined'],
#             'might': skill['might'],
#             'restrictedTo': {'moveType': inheritable_movement, 'weaponType': inheritable_weapons},
#             'sp': skill['sp_cost'],
#             'score': skill['score'],
#             'cooldown': 0,
#             'stats': skill['stats']
#         }
#     except KeyError:
#         # traceback.print_exc()
#         pass
#     except Exception:
#         traceback.print_exc()
#         pass