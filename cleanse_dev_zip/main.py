from os import makedirs
from os.path import isfile, isdir, join, sep, split
from zipfile import ZipFile

OUT_DIR = './out'
IGNORES = [
  '/venv/', 
  '/node_modules/', 
  '/.svelte-kit/', 
  '/.git/', 
  '/.cache/', 
  '/.next/', 
  '.gitignore', 
]

def should_ignore(item):
  for ignore in IGNORES:
    if ignore in item:
      return True
  return False

dev_zip = ZipFile('dev.zip')

with open('log.csv', 'w') as w:
      w.write('')
print(sep)

with open('log.csv', 'a') as a:
  for item in dev_zip.namelist():

    if not(should_ignore(item)):
      a.write(item + '\n')
      head, tail = split(item)
      
      try:
        makedirs(head)
      except Exception as e:
        # print('ERROR', 'makedirs', e)
        pass
      
      if tail:
        try:
          dev_zip.extract(item)
        except Exception as e:
          print('ERROR', 'extract', e)
