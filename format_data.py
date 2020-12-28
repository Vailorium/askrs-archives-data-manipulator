import json, os
import extract_data, manage_heroes, manage_skills

# Raw Data Variables
translations = extract_data.getTranslations()
raw_skill_list = extract_data.getRawSkills()
with open('y.json', 'w', encoding='utf-8') as outfile:
    json.dump(raw_skill_list, outfile, ensure_ascii=False)
raw_hero_list = extract_data.getRawHeroes()
seal_list = extract_data.getSealData() # returns [seal sid, is max tier skill (bool)]
resplendent_hero_list = extract_data.getResplendentData() # returns list of hero pid who are resplendents
refine_dictionary = extract_data.getRefineDictionary() # gets refine list "weapon id": ["refine ids"]

# Hero Data
hero_list = manage_heroes.generateHeroList(raw_hero_list)
hero_dict = manage_heroes.generateHeroDict(hero_list)

# Skill Data
skill_list = manage_skills.generateSkillList(raw_skill_list, hero_list)
skill_dict = manage_skills.generateSkillDict(skill_list)
hero_dict, refine_skills, skill_dict = manage_skills.getRefineSkills(skill_dict, refine_dictionary, hero_dict)

skill_list = manage_skills.skillListFromSkillDict(skill_dict)

# updating hero data
hero_list = manage_heroes.heroListfromHeroDict(hero_dict)

# max tier skills
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