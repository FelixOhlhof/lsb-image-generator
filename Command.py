from multiprocessing import Queue
import numpy

class Command:
    """
    Represents a Command from the ini file
    """
    def __init__(self, command_name, command_text, iterators, variables, init_commands_lazy = False):
        self.command_name = command_name
        self.command_text = command_text
        self.iterators = iterators
        self.variables = variables
        self.command_queue = Queue()
        self.current_command = None
        self.init_commands_lazy = init_commands_lazy
        if(init_commands_lazy):
            self.next_iterators = self.get_next_iterator_combination_lazy()
            for _ in range(numpy.prod([len(i.values) for i in self.iterators])):
                self.command_queue.put(0)
        else:
            self.fill_comand_queue(self.iterators)
        pass
        

    def has_next(self):
        return not self.command_queue.empty()

    def get_next(self):
        if self.init_commands_lazy:
            self.current_command = self.get_next_cmd(next(self.next_iterators))
            return self.current_command, [[i.name, i.get_current_value()] for i in self.iterators]
        if self.command_queue.empty(): 
            raise Exception('no iteratable values existing')
        self.current_command = self.command_queue.get()
        return self.current_command[0], self.current_command[1]
    
    def get_next_iterator_combination_lazy(self):
        iterator_values = [i.values for i in self.iterators]
        n = len(iterator_values)
        indices = [0] * n
        
        while True:
            next_iterator_combination = []
            for i in range(n):
                if(not self.iterators[i].has_next()):
                    self.iterators[i].init_queue()
                if(not self.iterators[i].get_current_value()):
                    self.iterators[i].get_next()
                next_iterator_combination.append(self.iterators[i])
            self.command_queue.get()
            yield next_iterator_combination
        
            # Update indices to get the next combination
            for i in range(n - 1, -1, -1):
                indices[i] += 1
                self.iterators[i].get_next()
                # self.iterators[i].get_next()
                if indices[i] < len(iterator_values[i]):
                    break
                indices[i] = 0
            else:
                # All combinations have been generated
                return

    def get_next_cmd(self, iterators):
        current_cmd = self.command_text
        for iterator in iterators:
            current_cmd = current_cmd.replace(iterator.text, iterator.get_current_value())
            for iterator_variable in iterator.variables:
                current_cmd = current_cmd.replace(iterator_variable.text, iterator_variable.get_value(iterator))
        for variable in self.variables:
            current_cmd = current_cmd.replace(variable.text, variable.get_value())
        if(current_cmd.__contains__('[$')):
            raise Exception(f'Could not apply all variables and iterators of command: {current_cmd}')    
        return current_cmd

    def fill_comand_queue(self, iterators, current_combination=[]):
        if not iterators:
            current_cmd = self.get_next_cmd(current_combination)
            self.command_queue.put([current_cmd, [[i.name, i.get_current_value()] for i in current_combination]])
            return

        while iterators[0].has_next():
            iterators[0].get_next()
            tmp = current_combination + [iterators[0]]
            self.fill_comand_queue(iterators[1:], tmp)
        iterators[0].init_queue()

    