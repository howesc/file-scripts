import os
from shutil import copy, copy2, move
import random
import string

def randomString():
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

walk_path = 'D:/Dropbox/Samples/Computer Music'
library_path = 'D:/Dropbox/Samples/Computer Music'

for source_dir, _, files in os.walk(walk_path):

  print(source_dir)

  for file_name in files:

    file_name = file_name.split('.')
    
    try:
      source_path = source_dir + '/' + file_name[0] + '.' + file_name[1]
      target_path = library_path + '/' + file_name[0] + '.' + file_name[1]
    except Exception as e:
      print('ERROR', source_dir, file_name)
      print(e)
      continue

    try:
      move(source_path, target_path)
    except:
      try:
        target_path = library_path + '/' + file_name[0] + '_' + randomString() + '.' + file_name[1]
      except Exception as e:
        print('ERROR', source_dir, file_name)
        print(e)
        continue
  
  print(len(os.listdir(source_dir)))
  if len(os.listdir(source_dir)) == 0:
      # removing the file using the os.remove() method
      os.rmdir(source_dir)