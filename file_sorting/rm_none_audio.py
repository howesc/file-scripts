import os

walk_path = os.path.join('D:', 'Dropbox', 'Music', 'iTunes', 'Music')

for source_dir, _, files in os.walk(walk_path):

  for file_name in files:

    source_path = os.path.join(source_dir, file_name)

    if not file_name.lower().endswith(('mp3', 'm4a', 'aif', 'wav')):
      os.remove(source_path)
      continue