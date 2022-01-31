import os


walk_path = 'D:/Dropbox/Pictures'

extensions = {}

for source_dir, _, files in os.walk(walk_path):
    
    print(source_dir)

    for file_name in files:

        extension  = os.path.splitext(file_name)[1]
    
        if extension not in extensions:
            extensions[extension] = 1
        else:
            extensions[extension] += 1

print(extensions)