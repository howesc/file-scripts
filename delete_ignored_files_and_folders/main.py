from os import makedirs, walk, remove
from os.path import isfile, isdir, join, sep, split

ROOT_DIR = './'

DELETE_FOLDERS = [
  'venv', 
  '__pycache__', 
  'node_modules', 
  '.svelte-kit', 
  '.git', 
  '.cache', 
  '.next', 
]

DELETE_FILES = [
  '.gitignore', 
]

with open('log.csv', 'w') as w:
      w.write('')

with open('log.csv', 'a') as a:
  for dirpath, dirnames, filenames in walk(ROOT_DIR):

    # for dirname in dirnames:
    #   if len([delete_folder for delete_folder in DELETE_FOLDERS if delete_folder == dirname]):
    #     a.write(dirpath + ',' + dirname + '\n')

    for filename in filenames:
      if len([delete_file for delete_file in DELETE_FILES if delete_file == filename]):
        # remove(join(dirpath, filename))
        a.write(dirpath + ',' + filename + '\n')
