from multiprocessing import Queue
import copy

class Command:
    def __init__(self, command_text, iterators, variables):
        self.command_text = command_text
        self.iterators = iterators
        self.variables = variables
        self.command_queue = Queue()
        self.current_command = None

        self.fill_comand_queue(self.iterators)
        print(f'Successfully added {self.command_queue.qsize()} items to command queue of command: {self.command_text}!')

    def has_next(self):
        return not self.command_queue.empty()

    def get_next(self):
        if self.command_queue.empty(): 
            raise Exception('no iteratable values existing')
        self.current_command = self.command_queue.get()
        return self.current_command
    
    def fill_comand_queue_lazy(self, iterators, current_combination=[]):
        if not iterators:
            self.command_queue.put([copy.copy(i) for i in current_combination]) # need deepcopy but not possible with queue 
            return

        while iterators[0].has_next():
            iterators[0].get_next()
            tmp = current_combination + [iterators[0]]
            self.fill_comand_queue_lazy(iterators[1:], tmp)
        iterators[0].init_queue()
    
    def fill_comand_queue(self, iterators, current_combination=[]):
        if not iterators:
            current_cmd = self.command_text
            for iterator in current_combination:
                current_cmd = current_cmd.replace(iterator.text, iterator.current_value)
                for iterator_variable in iterator.variables:
                    current_cmd = current_cmd.replace(iterator_variable.text, iterator_variable.get_value())
            for variable in self.variables:
                current_cmd = current_cmd.replace(variable.text, variable.get_value())
            if(current_cmd.__contains__('[$')):
                raise Exception(f'Could not apply all variables and iterators of command: {current_cmd}')
            self.command_queue.put(current_cmd)
            return

        while iterators[0].has_next():
            iterators[0].get_next()
            tmp = current_combination + [iterators[0]]
            self.fill_comand_queue(iterators[1:], tmp)
        iterators[0].init_queue()

    