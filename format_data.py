import json, os
import extract_data, manage_heroes, manage_skills

# Raw Data Variables
translations = extract_data.getTranslations()
raw_skill_list = extract_data.getRawSkills()
raw_hero_list = extract_data.getRawHeroes()
seal_list = extract_data.getSealData() # returns [seal sid, is max tier skill (bool)]
resplendent_hero_list = extract_data.getResplendentData() # returns list of hero pid who are resplendents
refine_dictionary = extract_data.getRefineDictionary() # gets refine list "weapon id": ["refine ids"]

# Hero Data
hero_list = manage_heroes.generateHeroList(raw_hero_list)
hero_dict = manage_heroes.generateHeroDict(hero_list)

skill_id_num_map = {}
for skill in raw_skill_list:
    if skill['id_num'] not in skill_id_num_map.keys():
        skill_id_num_map[skill['id_num']] = skill['id_tag']
    else:
        print("ERROR: KEY ALREADY EXISTS")

hero_id_num_map = {}
for hero in raw_hero_list:
    if hero['id_num'] not in hero_id_num_map.keys():
        hero_id_num_map[hero['id_num']] = hero['id_tag']
    else:
        print("ERROR: KEY ALREADY EXISTS")

# Skill Data
skill_list = manage_skills.generateSkillList(raw_skill_list, hero_list)
skill_dict = manage_skills.generateSkillDict(skill_list)
hero_dict, refine_skills, skill_dict = manage_skills.getRefineSkills(skill_dict, refine_dictionary, hero_dict)

skill_list = manage_skills.skillListFromSkillDict(skill_dict)

hero_list = manage_heroes.heroListfromHeroDict(hero_dict)

max_tier_skills_by_category = manage_skills.getMaxTierSkills(raw_skill_list, hero_list, seal_list)

# Export Data
try:
    os.mkdir('./output')
except FileExistsError:
    pass # dir already exists

with open('./output/hero_list.json', 'w', encoding='utf-8') as outfile:
    json.dump(hero_list, outfile, ensure_ascii=False)
with open('./output/hero_dictionary.json', 'w', encoding='utf-8') as outfile:
    json.dump(hero_dict, outfile, ensure_ascii=False)

with open('./output/skill_list.json', 'w', encoding='utf-8') as outfile:
    json.dump(skill_list, outfile, ensure_ascii=False)
with open('./output/skills.json', 'w', encoding='utf-8') as outfile:
    json.dump(skill_dict, outfile, ensure_ascii=False)
with open('./output/max_tier_skills_by_categories.json', 'w', encoding='utf-8') as outfile:
    json.dump(max_tier_skills_by_category, outfile, ensure_ascii=False)
with open('./output/refine_skill_data.json', 'w', encoding='utf-8') as outfile:
    json.dump(refine_skills, outfile, ensure_ascii=False)

with open('./output/hero_id_num_map.json', 'w', encoding='utf-8') as outfile:
    json.dump(hero_id_num_map, outfile, ensure_ascii=False)
with open('./output/skill_id_num_map.json', 'w', encoding='utf-8') as outfile:
    json.dump(skill_id_num_map, outfile, ensure_ascii=False)