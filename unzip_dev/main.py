import zipfile
from os import makedirs
from os.path import isdir
from shutil import copy2

dev_zip = zipfile.ZipFile('dev.zip')

def include_in_extraction(item):
  excludes = [
    '/node_modules/', 
    '.git', 
    '/venv/', 
  ]
  
  include = True
  for exclude in excludes:
    if exclude in item:
      include = False
  
  return include


for item in dev_zip.namelist():

  if include_in_extraction(item):
    with open('log.csv', 'a') as a:
      a.write(item + '\n')

    if not(isdir(item)):
      makedirs(item)
    
    try:
      dev_zip.extract(item, item)
      # print('extracted', item)
    except Exception as e:
      print('ERROR', e)
