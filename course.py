from os import listdir
from os.path import isfile

class Course():
    def __init__(self, name):
        dirs = [dir for dir in listdir() if not isfile(dir) and not dir[0] in [".", "_"]]
        self.name = name
        self.exists = name in dirs
