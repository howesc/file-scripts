import os
import random
import string
from shutil import copy2, move

def randomString():
  # return ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
  return random.choice(string.ascii_lowercase) + random.choice(['a', 'e', 'i', 'o', 'u']) + random.choice(string.ascii_lowercase) + random.choice(['a', 'e', 'i', 'o', 'u'])

# walk_dir = '/Users/chrishowes/Dropbox/Samples/Pads'
# target_dir= '/Users/chrishowes/Dropbox/Samples/Pads - flat'

# for source_dir, _, files in os.walk(walk_dir):
#   print(source_dir)

#   for file_name in files:

#     try:
#       file_name = file_name.split('.')
#       copy2(os.path.join(source_dir, file_name[0] + '.' + file_name[1]), target_dir)
#     except:
#       try:
#         copy2(os.path.join(source_dir, file_name[0] + '_' + randomString() + '.' + file_name[1]), target_dir)
#       except:
#         print('ERROR', 'copy2', source_dir, file_name)
#         continue
#       quit()

walk_dir = '/Users/chrishowes/Dropbox/Samples/Samplephonics Drums'
target_dir = '/Users/chrishowes/Dropbox/Samples/Samplephonics Drums - flat'

for source_dir, _, files in os.walk(walk_dir):
  print(source_dir)

  for file_name in files:

    try:
      file_name = file_name.split('.')
    except:
      continue

    try:
      if file_name[-1] in ['wav', 'aif']:
        copy2(os.path.join(source_dir, file_name[0] + '.' + file_name[1]), target_dir)
    except:
      try:
        copy2(os.path.join(source_dir, file_name[0] + '_' + randomString() + '.' + file_name[1]), target_dir)
      except:
        print('ERROR', 'copy2', source_dir, file_name)
        continue
      # print('ERROR', 'copy2', source_dir, file_name)
      # continue


# walk_dir = '/Users/chrishowes/Dropbox/Samples/Computer Music - flat'
# target_dir= '/Users/chrishowes/Dropbox/Samples/Computer Music - chunks'

# n = 795
# i = 0
# for source_dir, _, files in os.walk(walk_dir):
  
#   print(source_dir)

#   for file_name in files:

#     id = ('000' + str(i % n))[-3:]
#     target_path = os.path.join(target_dir, id)
#     if not os.path.exists(target_path):
#       os.makedirs(target_path)

#     try:
#       copy2(os.path.join(source_dir, file_name), target_path)
#     except:
#       print('ERROR', 'copy2', source_dir, file_name)
#       continue

#     i += 1


# notes = ['A', 'A#', 'B', 'B#', 'C', 'C#', 'D', 'D#', 'E', 'E#', 'F', 'F#', 'G', 'G#']
# octs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', ]

# notesocts = []
# for note in notes:
#   for oct in octs:
#     notesocts.append(note + oct)

# nums = []
# for num in range(100):
#   nums.append(('00' + str(num))[-2:])

# print(nums)

# walk_dir = '/Users/chrishowes/Dropbox/Samples/Kontakt 3/homeless'
# target_dir = '/Users/chrishowes/Dropbox/Samples/Kontakt 3'

# for source_dir, _, files in os.walk(walk_dir):

#   print(source_dir)

#   for file_name in files:

#     try:
#       ext = file_name.split('.')[-1].lower()
#       if ext not in ['wav', 'aif']:
#         raise Exception
#     except:
#       print('ERROR', 'ext', source_dir, file_name)
#       continue
    
#     # f = file_name[:-4].upper()
#     f = file_name.split('.')[0].upper()

#     def copy_to_dir(dir):
#       target_path = os.path.join(target_dir, dir)
#       if not os.path.exists(target_path):
#         os.makedirs(target_path)
#       try:
#         move(os.path.join(source_dir, file_name), target_path)
#       except:
#         print('ERROR', 'copy_to_dir', source_dir, file_name)
        
#     def search_all_slots(delimiter):
#       ls = f.split(delimiter)
#       for l in reversed(ls):
#         if l in notesocts:
#           return l
#       return None
    
#     def search_last_slot(delimiter):
#       ls = f.split(delimiter)
#       if ('00' + ls[-1])[-2:] in nums:
#         return ('00' + ls[-1])[-2:]
#       return None
    
#     def contains_noteoct():
#       for noteoct in notesocts:
#         if noteoct in f:
#           return noteoct
#       return None

#     if search_all_slots('_'):
#       copy_to_dir(search_all_slots('_'))
#       continue
#     elif search_all_slots(' '):
#       copy_to_dir(search_all_slots(' '))
#       continue
#     elif search_all_slots('-'):
#       copy_to_dir(search_all_slots('-'))
#       continue
#     elif 'BPM' in f or 'LOOP' in f:
#       copy_to_dir('loops')
#       continue
#     elif search_last_slot('_'):
#       copy_to_dir(search_last_slot('_'))
#       continue
#     elif search_last_slot(' '):
#       copy_to_dir(search_last_slot(' '))
#       continue
#     elif search_last_slot('-'):
#       copy_to_dir(search_last_slot('-'))
#       continue
#     elif search_last_slot('.'):
#       copy_to_dir(search_last_slot('.'))
#       continue
#     elif contains_noteoct():
#       copy_to_dir(contains_noteoct())
#       continue
#     else:
#       copy_to_dir('homeless')
#       continue
