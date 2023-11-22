import os
from os.path import isfile, join

class Path:
    def __init__(self, args):
        self.name = "Path"
        self.path = args[0]
        self.values = [join(self.path, f) for f in os.listdir(self.path) if isfile(join(self.path, f))]

    
class Integer:
    def __init__(self, args):
        self.name = "Integer"
        self.values = []
        self.start = int(args[0])
        self.end = int(args[1])
        self.step = int(args[2])

        for i in range(self.start, self.end, self.step):
            self.values.append(str(i))
