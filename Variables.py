
class Variable:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.__value = kwargs.get('value', None) # only accessable throug getter
        self.is_constant = kwargs.get('is_constant', True)
        self.recalculate_on_get = kwargs.get('recalculate_on_get', False)

    def get_value(self):
        #if(self.is_constant):
            # These are thread specific and changable variables like current file or current task. 
        # 
            #self.local_variables = dict()
            #return self.local_variables[self.name]
        return self.__value
    
    


# Implement new Variables here 

from datetime import datetime
class Date(Variable):
    def __init__(self, **kwargs):
        kwargs['name'] = 'date'
        if(kwargs.get('value', None) is None):
            kwargs['value'] = str(datetime.date)
        super().__init__(**kwargs)

    def get_value(self):
        if(super().recalculate_on_get):
            return str(datetime.date)
        return super().get_value()
    
class DateTime(Variable):
    def __init__(self, **kwargs):
        kwargs['name'] = 'datetime'
        if(kwargs.get('value', None) is None):
            kwargs['value'] = str(datetime.now())
        super().__init__(**kwargs)

    def get_value(self):
        if(self.recalculate_on_get):
            return str(datetime.now())
        return super().get_value()
    
class Task(Variable):
    def __init__(self, **kwargs):
        kwargs['name'] = 'task'
        kwargs['is_constant'] = False
        super().__init__(**kwargs)

    def get_value(self):
        return super().get_value()
    
class File(Variable):
    def __init__(self, **kwargs):
        kwargs['name'] = 'file'
        kwargs['is_constant'] = False
        super().__init__(**kwargs)

    def get_value(self):
        return super().get_value()