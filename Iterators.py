import os
from queue import Queue # due to python bug normal queue must be used
from os.path import isfile, join
from Variables import *

class IteratorBase:
    """
    Base class for iterators.
    
    How to add iterators: 
    1. Add a class to this file which must derive from IteratorBase.
    2. Give the class a static property called 'name'. The name must start with a big letter. This is the name you can use in the ini file.
    3. Define an init function like so: def __init__(self, args, variables = None). 
        args  :  list
            The arguments passed in the init file after ':' and seperated by ';'
        variables (optional)  :   list of Variables
            You can implement variables for iterators which get updated each time the 'iteraterator.get_next()' method was called. The variable than must implement the 'set_value(iterator)' method.
            You dont need to add this parameter to the __init__ function. 
            If you just want your current iterator value you can use the [$YourIterator.current_value] variable in the command text. 
    4. Implement the init function how ever you want. Just call super().__init__(values, variables) at the end. 
    """

    text = ''

    def __init__(self, values, variables=None):
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

    def __init__(self, args, variables = None):
        try:
            self.path = args[0]
            extensions = None
            try: extensions = args[1].lower().split(',') 
            except: pass
            values = [join(self.path, f) for f in os.listdir(self.path) if isfile(join(self.path, f)) and (f.endswith(tuple(extensions)) if extensions else True)]
            try: values = values[int(args[2].split(',')[0]): int(args[2].split(',')[1])]
            except: pass
            if variables is None:
                variables = [CurrentValue(), CurrentFileName()]

            super().__init__(values, variables)

        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Iterator: {error}")
    
    def get_current_value(self, with_quotes=False):
        if with_quotes:
            return f'"{super().get_current_value()}"'
        else:
            return super().get_current_value()

    
class Integer(IteratorBase):
    name = "Integer"
    
    def __init__(self, args, variables = None):
        try:
            values = []
            self.start = int(args[0])
            self.end = int(args[1])
            self.step = int(args[2])

            for i in range(self.start, self.end, self.step):
                values.append(str(i))
            if variables is None:
                variables = [CurrentValue()]

            super().__init__(values, variables)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Iterator: {error}")
