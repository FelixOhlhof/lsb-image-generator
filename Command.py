import queue
import re
import os
import itertools
import copy
from Settings import Settings

class Command:
    def __init__(self, command_text, iterators, variables):
        self.command_text = command_text
        self.iterators = iterators
        self.variables = variables
        self.command_queue = queue.Queue()

        # self.fill_comand_queue(self.iterators)
        print(f'Successfully added {self.command_queue.qsize()} items to command queue of command: {self.command_text}!')


    def fill_comand_queue(self, iterators, current_combination=[]):
        if not iterators:
            self.command_queue.put([copy.copy(i) for i in current_combination]) # need deepcopy but not possible with queue 
            return

        while iterators[0].has_next():
            iterators[0].get_next()
            tmp = current_combination + [iterators[0]]
            self.fill_comand_queue(iterators[1:], tmp)
        iterators[0].init_queue()
    
    def run_commands(self, iterators, current_combination=[]):
        if not iterators:
            
            print()
            return

        while iterators[0].has_next():
            iterators[0].get_next()
            tmp = current_combination + [iterators[0]]
            self.run_commands(iterators[1:], tmp)
        iterators[0].init_queue()

    def tmppp(self):
        for i in iterators:
            tmp.append([f"{i.name}::{f}" for f in i.values])
        all_combinations = [p for p in itertools.product(*tmp)]

        for iterator_combination in all_combinations:
            cmd_variant = command_text
            if(not self.iterators is None):
                for iterator_item in iterator_combination:
                    iterator_item_name = iterator_item[0:iterator_item.index("::")]
                    iterator_item_value = iterator_item[iterator_item.index("::")+2:]
                    tmp_iterator_name = 'tmptmptmptmp'
                    cmd_variant = re.sub(r"\[\$" + iterator_item_name + r":.*?\]", tmp_iterator_name, cmd_variant).replace(tmp_iterator_name, iterator_item_value)
                    if(iterator_item_name == 'Path'):
                        # TODO: add iterator related variables to Iterator
                        from Variables import CurrentFileName, CurrentFilePath
                        self.settings.local_variables[CurrentFilePath.name] = iterator_item_value
                        self.settings.local_variables[CurrentFileName.name] = os.path.basename(iterator_item_value)
            if(not self.variables is None):
                for var in self.variables:
                    cmd_variant = cmd_variant.replace(f"[${var.name}]", str(var.get_value()))
            if(cmd_variant.__contains__('[$')):
                raise Exception(f'Could not apply all variables and iterators of command: {cmd_variant}')
            self.command_queue.put(cmd_variant)

    def execute_all_command_variations(self):
        self.run_commands(self.iterators)