def extract_variables(command_text):
    import re
    import Variables

    variables = []

    vmatches = re.findall(r"\[\$[a-z].*?\]", command_text) # begins with lower case letter

    for match in vmatches:
        variable_name = re.search(r"(?<=\[\$)[a-z0-9-_]*(?=[:\]])", match)[0]
        # not fully functioning yes
        # variable_arguments = None
        # if ':' in match:
        #     variable_arguments = match[match.index(':')+1:match.index(']')].split(';')
        #     variable_arguments_dict = dict()
        #     variable_arguments_dict[variable_arguments[0].split('=')[0]] = variable_arguments[0].split('=')[1]
        #     print()
        variable = getattr(Variables, next(x[0] for x in [(name, cls) for name, cls in Variables.__dict__.items() if isinstance(cls, type)] if hasattr(x[1],'name') and x[1].name == variable_name))
        variable = variable() # initialize variable
        variables.append(variable)

    return variables

def extract_iterators(command_text):
    import re, string
    import Iterators

    iterators = []
    
    # matches = re.findall(r"\[\$[A-Z].*?\]", command_text) # begins with upper case letter
    matches = re.findall(r"\[\$[A-Z][A-Z]*[a-z0-9-_]*(?:[:].*?.*?(?=\])\]|(?=\])\])", command_text) # begins with upper case letter

    for match in matches:
        iterator_name = re.search(r"(?<=\[\$)[A-Z][A-Z]*[a-z0-9-_]*(?=[:\]])", match)[0]
        
        # extracts all iterator specific variables of the command
        iterator_variables = re.findall(rf"(?<={iterator_name}\.)[a-z0-9-_]*(?:[:].*?.*?(?=\])|(?=\]))", command_text)
        tmp_helper_str = ' '.join([f"[${v}]" for v in iterator_variables])
        iterator_variables = extract_variables(tmp_helper_str)
        
        cleaned = iterator_name.rstrip(string.digits)
        iterator = getattr(Iterators, cleaned)
        iterator.name = iterator_name
        iterator_arguments = None
        if ':' in match:
            iterator_arguments = match[match.index(':')+1:match.index(']')].split(';')
        iterators.append(iterator(iterator_arguments, iterator_variables))
    
    return iterators

def extract_parameters(command_text):
    pass

def parse_ini_file():
    import configparser
    import re
    import Iterators
    import Variables
    from Command import Command
    from Settings import Settings
    tasks = []

    config = configparser.ConfigParser()
    config.read('tasks.ini')
    
    for task in config.sections():
        settings = Settings()
        settings.local_variables[Variables.CurrentTaskName.name] = task # Add current task name to local variables 
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
                    v = v(settings=settings)
                    variables.append(v)
                commands.append(Command(command_text, iterators, variables, settings))
                print()

    return tasks

def get_tasks_from_ini_file(file):
    import configparser
    from Task import Task
    from Command import Command

    tasks = []

    config = configparser.ConfigParser()
    config.read(file)

    for task in [t for t in config.sections() if t != 'Settings']:
        task_name = task
        commands = []
        report_variables = []

        for line in config[task]:  
            if(line == 'command'):
                command_text = config[task][line]
                commands.append(Command(command_text, extract_iterators(command_text), extract_variables(command_text)))
            if(line == 'report'):
                pass

        tasks.append(Task(task_name, commands))

    return tasks
    