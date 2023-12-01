import os
import re
import shutil
import string
import Variables    
import Iterators
import configparser
from Task import Task
from Command import Command
from Settings import Settings

def extract_variables(command_text):
    variables = []

    vmatches = re.findall(r"\[\$[a-z].*?\]", command_text) # begins with lower case letter

    for match in vmatches:
        variable_name = re.search(r"(?<=\[\$)[a-z0-9-_]*(?=[:\]])", match)[0]
        variable = getattr(Variables, next(x[0] for x in [(name, cls) for name, cls in Variables.__dict__.items() if isinstance(cls, type)] if hasattr(x[1],'name') and x[1].name == variable_name))
        if ':' in match:
            variable = variable(match[match.index(':')+1:match.index(']')].split(';')) # initialize variable
        else:
            variable = variable()
        variable.text = match
        variables.append(variable)

    return variables

def extract_iterators(command_text):
    iterators = []
    
    # matches = re.findall(r"\[\$[A-Z].*?\]", command_text) # begins with upper case letter
    matches = re.findall(r"\[\$[A-Z][A-Z]*[a-z0-9-_]*(?:[:].*?.*?(?=\])\]|(?=\])\])", command_text) # begins with upper case letter

    for match in matches:
        iterator_name = re.search(r"(?<=\[\$)[A-Z][A-Z]*[a-z0-9-_]*(?=[:\]])", match)[0]
        
        # extracts all iterator specific variables of the command
        iterator_variables = re.findall(rf"(?<={iterator_name}\.)[a-z0-9-_]*(?:[:].*?.*?(?=\])|(?=\]))", command_text)
        tmp_helper_str = ' '.join([f"[${v}]" for v in iterator_variables])
        iterator_variables = extract_variables(tmp_helper_str)
        for v in iterator_variables:  v.text = f"[${iterator_name}.{v.text[2:]}"
        
        cleaned = iterator_name.rstrip(string.digits)
        iterator = getattr(Iterators, cleaned)
        iterator.name = iterator_name
        iterator_arguments = None
        if ':' in match:
            iterator_arguments = match[match.index(':')+1:match.index(']')].split(';')
        iterators.append(iterator(iterator_arguments, match, iterator_variables))
    
    return iterators

def extract_parameters(command_text):
    pass

def get_value_from_ini_file(section_name, setting_name):
    config = configparser.ConfigParser()
    config.read(Settings.CURRENT_INI_FILE)
    
    try:
        return config[section_name][setting_name]
    except Exception as error:
        raise(f"Could not retrieve Setting {section_name}:{section_name} from ini file: {error}")



def get_tasks_from_ini_file():
    tasks = []

    config = configparser.ConfigParser()
    config.read(Settings.CURRENT_INI_FILE)

    for task in [t for t in config.sections() if t not in Settings.INI_FILE_SYSTEM_SECTIONS]:
        task_name = task
        commands = []
        report_variables = []

        for line in config[task]:  
            if(line == Settings.INI_FILE_TASK_COMMAND):
                command_text = config[task][line]
                commands.append(Command(command_text, extract_iterators(command_text), extract_variables(command_text)))
            if(line == Settings.INI_FILE_TASK_REPORT):
                pass

        tasks.append(Task(task_name, commands))

    return tasks

def get_module_cmd(module_name):
    config = configparser.ConfigParser()
    config.read(Settings.CURRENT_INI_FILE)

    for module in [t for t in config.sections() if t == Settings.INI_FILE_SYSTEM_SECTIONS[1]]:
        for line in config[module]:  
            if(line.lower() == module_name.lower()):
                return config[module][line]
    raise Exception(f"Module {module_name} not found!")

def init():
    if not os.path.isfile(Settings.CURRENT_INI_FILE):
        shutil.copy(Settings.BASE_INI_FILE, Settings.CURRENT_INI_FILE)
    else:
        raise Exception(f"File task.ini already existing in {Settings.CURRENT_DIR}")