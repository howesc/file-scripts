import os

walk_path = os.path.join('D:', 'Dropbox', 'Music', 'iTunes')

for source_dir, _, files in os.walk(walk_path):

  for file_name in files:

    if file_name.lower().endswith(('ogg', 'mp3', 'm4a', 'aif', 'wav')):
      print(source_dir, file_name)