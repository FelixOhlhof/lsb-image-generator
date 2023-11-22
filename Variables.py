class VariableBase:
    def __init__(self, **kwargs):
        self.settings = kwargs.get('settings', None)
        self.name = kwargs.get('name', None)
        self.__value = kwargs.get('value', None) # only accessable through getter
        self.is_constant = kwargs.get('is_constant', True)
        self.is_global = kwargs.get('is_global', False)
        self.recalculate_on_get = kwargs.get('recalculate_on_get', False)

    def get_value(self):
        if(self.is_constant):
            return self.__value
        if(self.is_global):
            from Settings import Settings
            return Settings.shared_settings[self.name]
        return self.settings.local_variables[self.name]
    
    


# Implement new Variables here
# Each Variable must have a static property called "name" 
# The name MUST start with a small letter

from datetime import datetime
class Date(VariableBase):
    name = 'date'
    def __init__(self, **kwargs):
        kwargs['name'] = Date.name
        if(kwargs.get('value', None) is None):
            kwargs['value'] = str(datetime.date)
        super().__init__(**kwargs)

    def get_value(self):
        if(self.recalculate_on_get):
            return str(datetime.date)
        return super().get_value()
    
class DateTime(VariableBase):
    name = 'datetime'
    def __init__(self, **kwargs):
        kwargs['name'] = DateTime.name
        if(kwargs.get('value', None) is None):
            kwargs['value'] = str(datetime.now())
        super().__init__(**kwargs)

    def get_value(self):
        if(self.recalculate_on_get):
            return str(datetime.now())
        return super().get_value()
    
class Task(VariableBase):
    name = 'current_task'
    def __init__(self, **kwargs):
        kwargs['name'] = Task.name
        kwargs['is_constant'] = False
        kwargs['is_global'] = False # current task can not be global
        super().__init__(**kwargs)

    def get_value(self):
        return super().get_value()
    
class File(VariableBase):
    name = 'current_file'
    def __init__(self, **kwargs):
        kwargs['name'] = File.name
        kwargs['is_constant'] = False
        kwargs['is_global'] = False # current file can not be global
        super().__init__(**kwargs)

    def get_value(self):
        return super().get_value()
    
class FileName(VariableBase):
    name = 'current_file_name'
    def __init__(self, **kwargs):
        kwargs['name'] = FileName.name
        kwargs['is_constant'] = False
        kwargs['is_global'] = False # current file can not be global
        super().__init__(**kwargs)

    def get_value(self):
        return super().get_value()