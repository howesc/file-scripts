from os import walk, rmdir, path, sep

root = './copy-music-to-sd-card'

for dirpath, dirnames, filenames in walk(root):
  if len(dirnames) == 0 and len(filenames) == 0:
    print(dirpath, dirnames, filenames)
    rmdir(dirpath)
    