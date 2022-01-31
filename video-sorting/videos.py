import json
import os
from shutil import copy2

from json import dumps
from csv import DictWriter
from datetime import datetime
from dateutil.parser import parse

import exiftool_wrapper

# walk_path = 'D:/Dropbox/Pictures'
walk_path = 'E:/PRIVATE/AVCHD/BDMV/STREAM'
library_path = 'D:/Dropbox/Video Library'

fields = [
    'AverageHash',
    'ColorHash',
    'DateModified',
    'FileFileModifyDate',
    'EXIFCreateDate',
    'QuickTimeCreateDate',
    'Format',
    'ColorSpace',
    'Orientation',
    'FileSize',
    'XSize',
    'YSize',
    'Make',
    'Model',
    'Software',
    'HostComputer',
    'ImageDescription',
    'FileName',
    'SourceDir',
]

def get_metadatas():
    source_paths = []
    with open('output.csv', 'w', encoding='utf-8', newline='') as w:

        c = DictWriter(w, fields)
        c.writeheader()
        
        for source_dir, _, files in os.walk(walk_path):

            for file_name in files:

                if not file_name.lower().endswith(('.mts')):  # '.mov', '.mp4', '.avi', '.m4v', 
                    continue

                source_path = os.path.join(source_dir, file_name)
                source_paths.append(source_path)

    # print(source_paths)
    metadatas = []
    with exiftool_wrapper.ExifTool() as e:
        print('getting metadatas......')
        metadatas = e.get_metadata(*source_paths)
        open('metadatas.json', 'w', encoding='utf-8').write(json.dumps(metadatas, indent=2))


def copy_files():

    metadatas = json.loads(open('metadatas.json', 'r', encoding='utf-8').read())

    print('analysing metadatas......')
    with open('output.csv', 'w', encoding='utf-8', newline='') as w:

        c = DictWriter(w, fields)
        c.writeheader()

        for metadata in metadatas:

            source_path = metadata['SourceFile']
            file_name = metadata['File:FileName']
            
            d = {
                'AverageHash': None,
                'ColorHash': None,
                'DateModified': str(datetime.fromtimestamp(int(os.path.getmtime(source_path)))),
                'FileSize': str(metadata.get('File:FileSize', '')).strip(),
                'SourceDir': source_path,
                'FileName': file_name,
                'Format': str(metadata.get('File:FileType', '')).strip(),
                'XSize': str(metadata.get('File:ImageWidth', '')).strip(),
                'YSize': str(metadata.get('File:ImageHeight', '')).strip(),
            }

            d['ImageDescription'] = str(metadata.get('EXIF:ImageDescription', '')).strip()
            d['ColorSpace'] = str(metadata.get('EXIF:ColorSpace', '')).strip()
            d['Orientation'] = str(metadata.get('EXIF:Orientation', '')).strip()
            d['FileFileModifyDate'] = str(metadata.get('File:FileModifyDate', '')).strip()
            d['EXIFCreateDate'] = str(metadata.get('EXIF:CreateDate', '')).strip()
            d['QuickTimeCreateDate'] = str(metadata.get('QuickTime:CreateDate', '')).strip()
            d['Make'] = str(metadata.get('EXIF:Make', 'Unknown Make')).strip()
            d['Model'] = str(metadata.get('EXIF:Model', 'Unknown Model')).strip()
            d['Software'] = str(metadata.get('EXIF:Software', '')).strip()
            d['HostComputer'] = str(metadata.get('EXIF:HostComputer', '')).strip()

            c.writerow(d)
            # continue
            
            # print(d)
            # now copy file
            # 1) create year/month directory if directory not exists
            # 2) copy file to directory if file not exists

            # if d['CreateDate'] == '':
            #     timestamp = datetime.strptime(d['DateModified'], '%Y-%m-%d %H:%M:%S')
            # else:
            #     try:
            #         timestamp = datetime.strptime(d['CreateDate'], '%Y:%m:%d %H:%M:%S')
            #     except:
            #         timestamp = datetime.strptime(d['DateTime'], '%Y/%m/%d %H:%M:%S')

            print(source_path)

            try:
                timestamp = datetime.strptime(d['EXIFCreateDate'], '%Y:%m:%d %H:%M:%S')
            except:
                try:
                    timestamp =datetime.strptime(d['QuickTimeCreateDate'], '%Y:%m:%d %H:%M:%S')
                except:
                    timestamp =datetime.strptime(d['FileFileModifyDate'][:-6], '%Y:%m:%d %H:%M:%S')
            
            print(timestamp)

            year = str(timestamp.year)
            month = str(timestamp.month).zfill(2)
            day = str(timestamp.day).zfill(2)

            target_dir = os.path.join(library_path, d['Make'], d['Model'], year, month, day)

            # create the target directory if it doesn't already exist
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            target_path = os.path.join(target_dir, file_name)

            # copy the file and its metadata
            if not os.path.isfile(target_path):
                copy2(source_path, target_path)
            else:
                with open('errors.txt', 'w', encoding='utf-8') as w:
                    w.write(','.join(['file name already exists in target_path', source_path, target_path]))


get_metadatas()
copy_files()