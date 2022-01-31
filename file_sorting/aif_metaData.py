# encoding=<Encoding.LATIN1: 0>

import os
from shutil import copy2, move
from pydub import AudioSegment

import mutagen
from mutagen import mp4, easymp4, mp3, aiff

class AifMetaData:
  def __init__(self, fl):
    self.title = str(fl.get('TIT2', None))
    self.artist = str(fl.get('TPE1', None))
    self.albumArtist = str(fl.get('TPE2', None))
    self.composer = str(fl.get('TCOM', None))
    self.album = str(fl.get('TALB', None))
    self.trackNo = str(fl.get('TRCK', None)[0]).split('/')[0]
    self.tracks = str(fl.get('TRCK', None)[0]).split('/')[1]
    self.diskNo = str(fl.get('TPOS', None)[0]).split('/')[0]
    self.disks = str(fl.get('TPOS', None)[0]).split('/')[1]
    self.genre = str(fl.get('TCON', None))
    self.year = str(fl.get('TDRC', None))

  def summary(self):
    varsCopy = vars(self).copy()
    return varsCopy

walk_path = os.path.join('G:', 'My Drive', 'Music', 'aif by Album')

for source_dir, _, files in os.walk(walk_path):

    try:
      print(source_dir)
    except:
      continue
    
    for file in files:

        fileName = file.split('.')[:-1]
        fileExt = file.split('.')[-1]
        print(fileName, fileExt)
        quit()
        
        if not file.lower().endswith(('aif')):
          continue

        source_path = os.path.join(source_dir, file)
        
        mut = aiff.AIFF(source_path)
        metaData = AifMetaData(mut)

        aif = AudioSegment.from_file(source_path)
