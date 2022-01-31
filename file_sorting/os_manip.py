import os
from shutil import copy2

source_path = 'foo'
target_path = 'bar'
name = 'test.txt'

# create the target path of it doesn't already exist
if not os.path.exists(target_path):
    os.makedirs(target_path)

# copy the file and its metadata
if not os.path.isfile(os.path.join(target_path, name)):
    copy2(
        os.path.join(source_path, name),
        os.path.join(target_path, name),
    )