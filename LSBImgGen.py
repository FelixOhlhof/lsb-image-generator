import os
import argparse
import configparser
import re
import Iterators
from Command import Command
from Variables import *
from Settings import Settings

class LSBImgGen:
    def __init__(self):
        pass

    def run(self):
        config = configparser.ConfigParser()
        config.read('tasks.ini')

        for task in config.sections():
            ctask = task
            commands = []
            for line in config[task]:  
                if(line == 'command'):
                    command_text = config[task][line]
                    imatches = re.findall(r"\[\$.*?:.*?\]", command_text)
                    iterators = []
                    for match in imatches:
                        if(str(match)[2].isupper()):
                            i = getattr(Iterators, str(match)[2:str(match).index(':')])
                            args = str(match)[str(match).index(':')+1:str(match).index(']')].split(';')
                            iterators.append(i(args))
                        settings = Settings()
                    commands.append(Command(command_text, iterators, [DateTime(value='g')]))
                    print()


if __name__=="__main__":
    gen = LSBImgGen()
    gen.run()