import os, json, traceback

#region SYSTEM
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
#endregion

#region GLOBALS
categories = ['weapon', 'assist', 'special', 'a', 'b', 'c', 's', 'Refine Weapon Skill Effect', 'Beast Transformation Effect']
weapons = ['sword', 'lance', 'axe', 'red_bow', 'blue_bow', 'green_bow', 'colorless_bow', 'red_dagger', 'blue_dagger', 'green_dagger', 'colorless_dagger', 'red_tome', 'blue_tome', 'green_tome', 'colorless_tome', 'staff', 'red_breath', 'blue_breath', 'green_breath', 'colorless_breath', 'red_beast', 'blue_beast', 'green_beast', 'colorless_beast']
movement_type = ['infantry', 'armor', 'cavalry', 'flying']
origins = ['heroes', 'shadow_dragon_new_mystery', 'echoes', 'genealogy', 'thracia', 'binding', 'blazing', 'sacred', 'path', 'dawn', 'awakening', 'fates', 'houses', 'mirage']
blessings = [None, 'fire', 'water', 'wind', 'earth', 'light', 'dark', 'astra', 'anima']

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
#endregion

#region DATA EXTRACTION
def getTranslations():
    id_translations = {}
    for filename in os.listdir('./extracted/files/assets/Common/SRPG/Skill'):
        try:
            with open('./extracted/files/assets/USEN/Message/Data/Data_'+filename, encoding='utf8') as json_file:
                data = json.load(json_file)
                for point in data:
                    id_translations[point['key']] = point['value']
        except Exception:
            traceback.print_exc()
            pass
    return id_translations

def getRawSkills(): # get's all skills (provided they are not ENEMY ONLY)
    raw_skill_list = []
    for filename in os.listdir('./extracted/files/assets/Common/SRPG/Skill'):
        try:
            with open('./extracted/files/assets/Common/SRPG/Skill/'+filename, encoding='utf8') as json_file:
                data = json.load(json_file)
                for point in data:
                    if point['enemy_only'] == False:
                        raw_skill_list.append(point)
        except Exception:
            traceback.print_exc()
            pass
    return raw_skill_list

def getRawHeroes():
    raw_hero_list = []
    for filename in os.listdir('./extracted/files/assets/Common/SRPG/Person'):
        try:
            with open('./extracted/files/assets/Common/SRPG/Person/'+filename, encoding='utf8') as json_file:
                data = json.load(json_file)
                for point in data:
                    raw_hero_list.append(point)
        except Exception:
            traceback.print_exc()
            pass
    return raw_hero_list

def getResplendentData():
    resplendent_hero_ids = []
    for filename in os.listdir('./extracted/files/assets/Common/SubscriptionCostume'):
        try:
            with open('./extracted/files/assets/Common/SubscriptionCostume/'+filename, encoding='utf8') as json_file:
                data = json.load(json_file)
                for point in data:
                    resplendent_hero_ids.append(point['hero_id'])
        except Exception:
            traceback.print_exc()
            pass
    return resplendent_hero_ids

def getSealData(): # Gets seal and if is max tier
    seal_sid = []
    for filename in os.listdir('./extracted/files/assets/Common/SRPG/SkillAccessory'):
            with open('./extracted/files/assets/Common/SRPG/SkillAccessory/'+filename, encoding='utf-8') as json_file:
                seal_data = json.load(json_file)
                for data in seal_data:
                    try:
                        seal_sid.append(['M'+data['id_tag'], data['next_seal'] == None])
                    except:
                        pass
    return seal_sid

def getRefineDictionary():
    refine_data = {}
    for filename in os.listdir('./extracted/files/assets/Common/SRPG/WeaponRefine'):
        with open('./extracted/files/assets/Common/SRPG/WeaponRefine/'+filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for weapon in data:
                if not weapon['orig'] in refine_data.keys():
                    refine_data[weapon['orig']] = []
                refine_data[weapon['orig']].append(weapon['refined'])
    return refine_data
#endregion

