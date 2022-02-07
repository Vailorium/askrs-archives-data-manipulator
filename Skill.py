import Utils

def handleSkillData():
  print("Loading Skill Data")
  walkedData = Utils.getWalkData('./extracted/files/assets/Common/SRPG/Skill')
  print("Skill Data Loaded")
  skillData = []
  print("Grouping Skill Data")
  for group in walkedData:
    for skill in group:
      skillData.append(skill)
  print("Saving data to ./output/skills/skill_list.json")
  Utils.saveJSONDataToFile(skillData, './output/skills/skill_list.json')

handleSkillData()