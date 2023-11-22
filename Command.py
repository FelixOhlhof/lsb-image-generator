import queue
import re
import itertools

class Command:
    def __init__(self, command_text, iterators, variables):
        self.command_text = command_text
        self.iterators = iterators
        self.variables = variables
        self.command_queue = queue.Queue()
        tmp = []

        for i in iterators:
            tmp.append([f"{i.name}::{f}" for f in i.values])
        all_combinations = [p for p in itertools.product(*tmp)]

        for iterator_combination in all_combinations:
            cmd_variant = command_text
            if(not self.iterators is None):
                for iterator_item in iterator_combination:
                    iterator_type = iterator_item[0:iterator_item.index("::")]
                    file_name = iterator_item[iterator_item.index("::")+2:]
                    tmp_file_name = 'tmptmptmptmp'
                    cmd_variant = re.sub(r"\[\$" + iterator_type + r":.*?\]", tmp_file_name, cmd_variant).replace(tmp_file_name, file_name)
            if(not self.variables is None):
                for param in self.parameter:
                    cmd_variant = cmd_variant.replace(f"[${param[0]}]", str(param[1]))
            if(cmd_variant.__contains__('[$')):
                raise Exception(f'Could not apply all parameter and iterators of command: {cmd_variant}')
            self.command_queue.put(cmd_variant)
        print()