import Utils, os

LOCALES = ['EUDE', 'EUEN', 'EUES', 'EUFR', 'EUIT', 'JPJA', 'TWZH', 'USEN', 'USES', 'USPT']

for locale in LOCALES:
  data = {}

  print("Loading Locale data: " + locale)
  walkedData = Utils.getWalkData('./extracted/files/assets/'+locale, ['Character', 'CrossLanguage', 'Embedded', 'Menu', 'Scenario'])
  print("Finished Loading Locale data for " + locale)

  print("Setting key-value data")
  for fileData in walkedData:
    for point in fileData:
      data[point['key']] = point['value']

  print('Saving to file output/locales/locale_'+locale+'.json')
  Utils.saveJSONDataToFile(data, 'output/locales/locale_'+locale+'.json')