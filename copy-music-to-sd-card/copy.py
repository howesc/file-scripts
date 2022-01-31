# copying music library from ubuntu to FAT sd
# FAT doesn't allow special characters in paths, so we must replace them

from os import walk, makedirs, path
from shutil import copy2

success = 0
error = 0

sourcedir = '/home/chris/Music'
targetdir = '/media/chris/128GB mSD/Music'

for dirpath, dirnames, filenames in walk(sourcedir):

  targetpath = dirpath.replace(sourcedir, targetdir).replace('*', '').replace('?', '').replace(':', ' -').replace('\"', ' -')
  
  try:
    makedirs(targetpath)
  except Exception as e:
    print('ERROR:', 'makedir', e)
    error += 1

  for filename in filenames:

    targetfilename = filename.replace('*', '').replace('?', '').replace(':', ' -').replace('\"', ' -')

    if not(path.isfile(path.join(targetpath, targetfilename))):

      try:
        copy2(path.join(dirpath, filename), path.join(targetpath, targetfilename))
        success += 1
        # pass
      except Exception as e:
        print('ERROR:', 'copy2', dirpath, filename, e)
        error += 1

print('success', success)
print('error', error)
