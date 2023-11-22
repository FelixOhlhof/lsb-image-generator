from Variables import *

class Settings:
    shared_settings = dict()

    def __init__(self):
        self.local_variables = dict()
        # self.local_variables[File.name] = None
        # self.local_variables[Task.name] = None