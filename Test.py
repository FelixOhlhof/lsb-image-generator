import os
import configparser
import re
import Iterators
from Command import Command
from Variables import *

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
            commands.append(Command(command_text, iterators, [DateTime()]))
            print()