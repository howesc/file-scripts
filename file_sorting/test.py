import os
from shutil import copy2

from json import dumps
from csv import DictWriter
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS
from imagehash import average_hash, colorhash

with open('TAGS.json', 'w', encoding='utf-8') as w:
    w.write(dumps(TAGS, indent='\t'))

walk_path = 'D:/Dropbox/Pictures/WDMyCloud/From Mac TM Backups/2018-01-04-203845/Photos Library/Originals/2016/05/20/20160520-102742'
library_path = 'D:/Dropbox/Photo Library'

fields = [
    'AverageHash',
    'ColorHash',
    'DateModified',
    'DateTime',
    'DateTimeOriginal',
    'DateTimeDigitized',
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

unique_combined_hashes = []
duplicates = []

with open('output.csv', 'w', encoding='utf-8', newline='') as w:

    c = DictWriter(w, fields)
    c.writeheader()
    
    for source_dir, _, files in os.walk(walk_path):

        print(source_dir)
        
        for file_name in files:

            if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                continue

            source_path = os.path.join(source_dir, file_name)
            im = Image.open(source_path)

            try:
                a_hash = average_hash(im, hash_size=16)
            except:
                with open('errors.txt', 'w', encoding='utf-8') as w:
                    w.write(','.join(['average_hash error', source_path]))
                a_hash = '0' * 64
            
            try:
                c_hash = colorhash(im, binbits=6)
            except:
                with open('errors.txt', 'w', encoding='utf-8') as w:
                    w.write(','.join(['color_hash error', source_path]))
                c_hash = '0' * 21

            d = {
                'AverageHash': str(a_hash),
                'ColorHash': str(c_hash),
                'DateModified': str(datetime.fromtimestamp(int(os.path.getmtime(source_path)))),
                'FileSize': os.path.getsize(source_path),
                'SourceDir': source_dir,
                'FileName': file_name,
                'Format': im.format,
                'XSize': im.size[0],
                'YSize': im.size[1],
            }

            combined_hash = d['AverageHash'] + d['ColorHash']

            is_duplicate = False
            if d['AverageHash'] + d['ColorHash'] not in unique_combined_hashes:
                unique_combined_hashes.append(combined_hash)
            else:
                is_duplicate = True
                duplicates.append(d)

            exifdata = im.getexif()
            
            d['ImageDescription'] = str(exifdata.get(270, '')).strip()
            d['ColorSpace'] = str(exifdata.get(40961, '')).strip()
            d['Orientation'] = exifdata.get(274, '')
            d['DateTime'] = str(exifdata.get(306, '')).strip()
            d['DateTimeOriginal'] = str(exifdata.get(36867, '')).strip()
            d['DateTimeDigitized'] = str(exifdata.get(36868, '')).strip()
            d['Make'] = str(exifdata.get(271, 'Unknown Make')).rstrip('\x00').strip()
            d['Model'] = str(exifdata.get(272, 'Unknown Model')).rstrip('\x00').strip()
            d['Software'] = str(exifdata.get(305, '')).strip()
            d['HostComputer'] = str(exifdata.get(316, '')).strip()
                
            c.writerow(d)

            if is_duplicate:
                continue

            # now copy file
            # 1) create year/month directory if directory not exists
            # 2) copy file to directory if file not exists

            if d['DateTime'] == '':
                timestamp = datetime.strptime(d['DateModified'], '%Y-%m-%d %H:%M:%S')
            else:
                try:
                    timestamp = datetime.strptime(d['DateTime'], '%Y:%m:%d %H:%M:%S')
                except:
                    timestamp = datetime.strptime(d['DateTime'], '%Y/%m/%d %H:%M:%S')
                
            year = str(timestamp.year)
            month = str(timestamp.month).zfill(2)
            day = str(timestamp.day).zfill(2)

            target_dir = os.path.join(library_path, d['Make'], d['Model'], year, month, day)
            # print(library_path, d['Make'], d['Model'], year, month, day)
            # print(exifdata[271].rstrip('\x00').encode('utf-16'))

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

with open('duplicates.json', 'w', encoding='utf-8') as w:
    w.write(dumps(duplicates, indent='\t'))