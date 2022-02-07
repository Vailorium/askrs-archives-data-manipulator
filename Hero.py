import Utils

def handleHeroData():
  print("Loading Hero Data")
  walkedData = Utils.getWalkData('./extracted/files/assets/Common/SRPG/Person')
  print("Hero Data Loaded")
  heroData = []
  print("Grouping Hero Data")
  for group in walkedData:
    for hero in group:
      heroData.append(hero)
  print("Saving data to ./output/heroes/hero_list.json")
  Utils.saveJSONDataToFile(heroData, './output/heroes/hero_list.json')

handleHeroData()