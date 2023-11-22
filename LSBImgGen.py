import os
import argparse
import configparser
import re
import Iterators
import Variables
from Variables import * 
from Command import Command
from Settings import Settings

class LSBImgGen:
    def __init__(self):
        pass

    def run(self):
        config = configparser.ConfigParser()
        config.read('tasks.ini')
        
        for task in config.sections():
            settings = Settings()
            settings.local_variables[Task.name] = task # Add current task name to local variables 
            commands = []
            for line in config[task]:  
                if(line == 'command'):
                    command_text = config[task][line]
                    imatches = re.findall(r"\[\$[A-Z].*?\]", command_text) # begins with upper case letter
                    iterators = []
                    for match in imatches:
                        if(str(match)[2].isupper()):
                            i = getattr(Iterators, str(match)[2:str(match).index(':')])
                            args = str(match)[str(match).index(':')+1:str(match).index(']')].split(';')
                            iterators.append(i(args))
                    variables = []
                    vmatches = re.findall(r"\[\$[a-z].*?\]", command_text) # begins with lower case letter
                    for match in vmatches:
                        v = getattr(Variables, next(x[0] for x in [(name, cls) for name, cls in Variables.__dict__.items() if isinstance(cls, type)] if hasattr(x[1],'name') and x[1].name == str(match)[2:-1]))
                        v = v()
                        variables.append(v)
                    commands.append(Command(command_text, iterators, variables, settings))
                    print()


if __name__=="__main__":
    gen = LSBImgGen()
    gen.run()