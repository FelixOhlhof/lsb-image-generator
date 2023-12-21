import os
import re
import shutil
import string
import Variables    
import Iterators
from Task import Task
from Command import Command
from Settings import Settings

"""Collection of useful methods"""

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
        iterator_arguments = None
        if ':' in match:
            iterator_arguments = match[match.index(':')+1:match.index(']')].split(';')
        iterator = iterator(iterator_arguments, iterator_variables)
        iterator.text = match
        iterator.name = iterator_name
        iterators.append(iterator)

    return iterators

def extract_parameters(command_text):
    pass

def get_value_from_ini_file(section_name, setting_name):    
    try:
        return Settings.INI_FILE[section_name][setting_name]
    except Exception as error:
        print(f"Could not retrieve Setting {section_name}:{section_name} from ini file: {error}")
        exit()

def get_int_from_ini_file(section_name, setting_name):    
    try:
        return int(Settings.INI_FILE[section_name][setting_name])
    except Exception as error:
        print(f"Could not retrieve Setting {section_name}:{section_name} from ini file: {error}")
        exit()
    
def get_bool_value_from_ini_file(section_name, setting_name):    
    try:
        true_values = ['true', '1', 't', 'y', 'yes', '-1']
        return Settings.INI_FILE[section_name][setting_name].lower() in true_values
    except Exception as error:
        print(f"Could not retrieve Setting {section_name}:{setting_name} from ini file: {error}")
        exit()



def get_tasks_from_ini_file():
    tasks = []
    for task in [t for t in Settings.INI_FILE.sections() if t not in Settings.INI_FILE_SYSTEM_SECTIONS]:
        task_name = task
        commands = []

        for line in Settings.INI_FILE[task]:  
            if(re.match(Settings.INI_FILE_COMMAND_NAME_PATTERN, line)):
                command_text = Settings.INI_FILE[task][line]
                commands.append(Command(re.match(Settings.INI_FILE_COMMAND_NAME_PATTERN, line).string, command_text, extract_iterators(command_text), extract_variables(command_text), Settings.GLOBAL_SETTINGS[Settings.INIT_COMMANDS_LAZY]))
            if(line == Settings.INI_FILE_TASK_REPORT):
                pass

        tasks.append(Task(task_name, commands))
    return tasks

def get_module_cmd(module_name):
    for module in [module for module in Settings.INI_FILE.sections() if module == Settings.INI_FILE_SECTION_MODULES]:
        for line in Settings.INI_FILE[module]:  
            if(line.lower() == module_name.lower()):
                cmd = Settings.INI_FILE[module][line]
                variables = extract_variables(Settings.INI_FILE[module][line])
                for variable in variables:
                    cmd = cmd.replace(variable.text, variable.get_value())
                return cmd
    print(f"Module {module_name} not found!")
    exit()

def get_complete_section_string(section_name):
    out = f"[{section_name}]\n"
    for line in Settings.INI_FILE[section_name]:  
        out += f"{line}={Settings.INI_FILE[section_name][line]}\n" 
    return out

def get_complete_task_section_string():
    out = ""
    for task in [t for t in Settings.INI_FILE.sections() if t not in Settings.INI_FILE_SYSTEM_SECTIONS]:
        out += f"[{task}]\n"
        for line in Settings.INI_FILE[task]:  
            out += f"{line}={Settings.INI_FILE[task][line]}\n"
    return out

def init():
    if not os.path.isfile(Settings.CURRENT_INI_FILE):
        shutil.copy(Settings.BASE_INI_FILE, Settings.CURRENT_INI_FILE)
    else:
        print(f"Error: File task.ini already existing in {Settings.CURRENT_DIR}")
        exit()