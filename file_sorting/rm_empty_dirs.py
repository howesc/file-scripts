import os

walk_path = os.path.join('D:', 'Dropbox', 'Music', 'iTunes', 'Music')

for source_dir, _, _ in os.walk(walk_path):

  if len(os.listdir(source_dir)) == 0:
    os.rmdir(source_dir)