import os
import argparse
import configparser
import re
import Iterators
import Variables
import Util
from Variables import * 
from Command import Command
from Settings import Settings

class LSBImgGen:
    def __init__(self):
        pass

    def run(self):
        pass


if __name__=="__main__":
    tasks = Util.get_tasks_from_ini_file('tasks.ini')
    for task in tasks:
        task.run_commands_single_threaded()