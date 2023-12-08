import os
from multiprocessing import Queue
from os.path import isfile, join
from Variables import *

class IteratorBase:
    def __init__(self, name, text, values, variables):
        self.name = name
        self.text = text
        self.values = values
        self.variables = variables        
        self.values_queue = Queue()
        self.__current_value = None
        self.init_queue()
    
    def init_queue(self):
        for value in self.values:
            self.values_queue.put(value)
        self.__current_value = None

    def has_next(self):
        return not self.values_queue.empty()

    def get_next(self):
        if self.values_queue.empty(): 
            raise Exception('no iteratable values existing')
        self.__current_value = self.values_queue.get()
        if self.variables: # update variables
            for variable in self.variables:
                variable.set_value(self)
        return self.__current_value
    
    def get_current_value(self):
        return self.__current_value
    
    def get_variable(self, variable_name):
        return [v for v in self.variables if v.name == variable_name][0]

# Implement new Iterators here
# Each Iterator must have a static property called "name" 
# The name MUST start with a capital letter and MUST NOT end with an number.

class Path(IteratorBase):
    name = 'Path'

    def __init__(self, args, text, variables = None):
        try:
            self.path = args[0]
            extensions = None
            if len(args) == 2:
                extensions = args[1].lower().split(',')
            values = [join(self.path, f) for f in os.listdir(self.path) if isfile(join(self.path, f)) and (f.endswith(tuple(extensions)) if extensions else True)]
            if variables is None:
                variables = [CurrentFilePath(), CurrentFileName()]

            super().__init__(Path.name, text, values, variables)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Iterator: {error}")
    
    def get_current_value(self, with_quotes=False):
        if with_quotes:
            return f'"{super().get_current_value()}"'
        else:
            return super().get_current_value()

    
class Integer(IteratorBase):
    name = "Integer"
    
    def __init__(self, args, text, variables = None):
        try:
            values = []
            self.start = int(args[0])
            self.end = int(args[1])
            self.step = int(args[2])

            for i in range(self.start, self.end, self.step):
                values.append(str(i))
            if variables is None:
                variables = [CurrentValue()]

            super().__init__(Integer.name, text, values, variables)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Iterator: {error}")
