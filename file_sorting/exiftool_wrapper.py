import subprocess
import os
import json

class ExifTool(object):

    sentinel = "{ready}\r\n"

    def __init__(self, executable="C:/Program Files/exiftool/exiftool(-k).exe"):
        self.executable = executable

    def __enter__(self):
        self.process = subprocess.Popen(
            [self.executable, "-stay_open", "True",  "-@", "-"],
            universal_newlines=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        return self

    def  __exit__(self, exc_type, exc_value, traceback):
        self.process.stdin.write("-stay_open\nFalse\n")
        self.process.stdin.flush()

    def execute(self, *args):
        args = args + ("-execute\n",)
        self.process.stdin.write(str.join("\n", args))
        self.process.stdin.flush()
        output = ""
        fd = self.process.stdout.fileno()
        while not output.endswith(self.sentinel):
            # print('os.read(fd, 4096)......', os.read(fd, 4096))
            output += os.read(fd, 4096).decode('utf-8')
        return output[:-len(self.sentinel)]

    def get_metadata(self, *filenames):
        # return self.execute("-G", "-j", "-n", *filenames)
        return json.loads(self.execute("-G", "-j", "-n", *filenames))



# file_names = ['D:/Dropbox/Pictures\WDMyCloud\From Mac TM Backups/2018-01-04-203845/Photos Library/Originals/2015/11/15/20151115-133014/MVI_3337.MOV']
# with ExifTool() as e:
#     metadata = e.get_metadata(*file_names)
#     # print(metadata['EXIF:Make'])
#     # print(metadata[0]['EXIF:Make'])
#     print(json.dumps(metadata, indent=' '))