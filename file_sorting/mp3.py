import os
from shutil import copy2, move

import mutagen
from mutagen import mp4, easymp4, mp3, aiff

# walk_path = os.path.join('Z:', 'CD Imports')
walk_path = os.path.join('D:', 'Dropbox', 'Music', 'iTunes', 'Podcasts')
# library_path = os.path.join('Z:', 'CD Imports by Album')
library_path = os.path.join('D:', 'Dropbox', 'Music', 'iTunes', 'mp3 by Album')

for source_dir, _, files in os.walk(walk_path):

    try:
      print(source_dir)
    except:
      continue
    
    for file_name in files:

        if not file_name.lower().endswith(('mp3')):
            continue

        source_path = os.path.join(source_dir, file_name)
        
        album = None
        try:
          if file_name.lower().endswith(('m4a')):
            fl = easymp4.MP4(source_path)
            album = fl[u'\xa9alb'][0]
          elif file_name.lower().endswith(('mp3')):
            fl = mp3.EasyMP3(source_path)
            album = fl['album'][0]
          elif file_name.lower().endswith(('aif')):
            fl = aiff.AIFF(source_path)
            album = fl['album'][0]
          else:
            fl = mutagen.File(source_path)
            print(fl)
            album = fl['album'][0]
        except:
          print('could not extract album name:', file_name)
          album = '_Unknown'

        album = str(album).strip().replace('/', '-').replace('\\', '-').replace(':', '-').replace('.', '-').replace('|', '-')

        target_dir = os.path.join(library_path, album)

        # create the target directory if it doesn't already exist
        if not os.path.exists(target_dir):
            try:
              os.makedirs(target_dir)
            except:
              print({
                'source_dir': source_dir,
                'file_name': file_name,
                'library_path': library_path,
                'album': album,
                })
              for c in target_dir:
                print(c)


        target_path = os.path.join(target_dir, file_name)

        # copy the file and its metadata
        if not os.path.isfile(target_path):
            move(source_path, target_path)
            if len(os.listdir(source_dir)) == 0:
              os.rmdir(source_dir)