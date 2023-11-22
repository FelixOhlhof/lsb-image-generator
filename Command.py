import queue
import re
import os
import itertools
from Settings import Settings

class Command:
    def __init__(self, command_text, iterators, variables, settings):
        self.command_text = command_text
        self.iterators = iterators
        self.variables = variables
        self.settings = settings
        self.command_queue = queue.Queue()
        tmp = []

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
                        self.settings.local_variables['current_file'] = iterator_item_value
                        self.settings.local_variables['current_file_name'] = os.path.basename(iterator_item_value)
            if(not self.variables is None):
                for var in self.variables:
                    cmd_variant = cmd_variant.replace(f"[${var.name}]", str(var.get_value()))
            if(cmd_variant.__contains__('[$')):
                raise Exception(f'Could not apply all variables and iterators of command: {cmd_variant}')
            self.command_queue.put(cmd_variant)
        print()