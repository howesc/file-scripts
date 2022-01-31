# encoding=<Encoding.LATIN1: 0>

import os
from shutil import copy2, move
from pydub import AudioSegment

import mutagen
from mutagen import mp4, easymp4, mp3, aiff, ogg

class AifMetaData:
  def __init__(self, fl):
    self.title = str(fl.get('TIT2', None))
    self.artist = str(fl.get('TPE1', None))
    self.albumArtist = str(fl.get('TPE2', None))
    self.composer = str(fl.get('TCOM', None))
    self.album = str(fl.get('TALB', None))
    self.track = str(fl.get('TRCK', None))
    # self.trackNo = str(fl.get('TRCK', ['1/1'])[0]).split('/')[0]
    # self.tracks = str(fl.get('TRCK', ['1/1'])[0]).split('/')[1]
    self.disk = str(fl.get('TPOS', None))
    # self.diskNo = str(fl.get('TPOS', ['1/1'])[0]).split('/')[0]
    # self.disks = str(fl.get('TPOS', ['1/1'])[0]).split('/')[1]
    self.genre = str(fl.get('TCON', None))
    self.year = str(fl.get('TDRC', None))

  def __str__(self):
    return str(self.summary())
  
  def summary(self):
    varsCopy = vars(self).copy()
    return varsCopy

walk_dir = os.path.join(os.path.sep, 'home', 'chris', 'Music', 'aif by Album')
library_dir = os.path.join(os.path.sep, 'home', 'chris', 'Music', 'ogg by Album')

for source_dir, _, files in os.walk(walk_dir):

    print(source_dir)
    
    for file in files:

      try:
        fileName = '.'.join(file.split('.')[:-1])
        fileExt = file.split('.')[-1]
        
        if fileExt != 'aif':
          continue

        source_path = os.path.join(source_dir, file)
        
        aifMut = aiff.AIFF(source_path)
        metaData = AifMetaData(aifMut)
        # print(metaData)

        
        album = metaData.album.strip().replace('/', '-').replace('\\', '-').replace(':', '-').replace('.', '-').replace('|', '-').replace('?', '')
        # if album == 'Drone':
        #   continue

        target_dir = os.path.join(library_dir, album)
        
        if not os.path.exists(target_dir):
          os.makedirs(target_dir)
        
        target_path = os.path.join(target_dir, '.'.join([fileName, 'ogg']))

        # copy the file and its metadata
        if not os.path.isfile(target_path):
        
          aifAud = AudioSegment.from_file(source_path)
          aifAud.export(target_path, 'ogg', bitrate='192k', id3v2_version=4, tags={
            'TITLE': metaData.title,
            'ARTIST': metaData.artist,
            'ALBUMARTIST': metaData.albumArtist,
            'COMPOSER': metaData.composer,
            'ALBUM': metaData.album,
            'GENRE': metaData.genre,
            'DATE': f'{metaData.year}-01-01T00:00:00Z',
            'TRACK': metaData.track,
            'DISCNUMBER': metaData.disk,
          })

          with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(album + ',' + file + '\n')

      except Exception as e:
        print(source_path, e)
        continue
        
        # quit()
