import os, json, errno

import time

def getDataFromFolder(folder):
  files = []
  for filename in os.listdir(folder):
    jsonFile = open(folder+'/'+filename, encoding='utf-8')
    files.append(json.load(jsonFile))
    jsonFile.close()
  return files

def saveJSONDataToFile(data, path):
  if not os.path.exists(os.path.dirname(path)):
      try:
          os.makedirs(os.path.dirname(path))
      except OSError as exc: # Guard against race condition
          if exc.errno != errno.EEXIST:
              raise

  with open(path, 'w', encoding='utf-8') as outFile:
    json.dump(data, outFile, ensure_ascii=False)

def getJSONDataFromFile(path):
  # print(path)
  jsonFile = open(path, encoding='utf-8')
  return json.load(jsonFile)

def getWalkData(path, blacklistDirs=[]):
  data = []
  for filename in os.listdir(path):
    if os.path.isdir(path + '/' + filename):
      if filename not in blacklistDirs:
        data = data + getWalkData(path + '/' + filename, blacklistDirs)
    else:
      jsonData = getJSONDataFromFile(path + '/' + filename)
      data.append(jsonData)
  return data