from datetime import datetime   
from pathlib import Path

class VariableBase:
    """
    Base class for Variables.
    
    How to add variables: 
    1. Add a class to this file which must derive from VariableBase.
    2. Give the class a static property called 'name'. The name must start with a small letter. This is the name you can use in the ini file.
    3. Define an init function like so: def __init__(self, args):. 
        args (optional)  :  list
            The arguments passed in the init file after ':' and seperated by ';'
    4. Implement the init function how ever you want. Just call super().__init__(...) at the end.
        You can pass the following parameters to the base class:
        value  :  dyn
            the value of the variable
        is_constant : bool
            if True returns a local setting named like the name of the variable
        is_global  :  bool
            if True returns a global setting named like the name of the variable
        include_in_report  : bool
            if True variable will be included in report
        recalculate_on_get  : bool
            if True variable will be recalculated on get_value() method. You need to overwrite the get_value() method and check if recalculate_on_get is True.
        Usually you just pass the value parameter. 
    """

    text = ''

    def __init__(self, **kwargs):
        self.settings = kwargs.get('settings', None)
        self.__value = kwargs.get('value', None) # only accessable through getter
        self.is_constant = kwargs.get('is_constant', False)
        self.is_global = kwargs.get('is_global', False)
        self.include_in_report = kwargs.get('include_in_report', True)
        self.recalculate_on_get = kwargs.get('recalculate_on_get', False)

    def get_value(self, *args):
        if(self.is_constant):
            return self.settings.get_value(self.name)
        if(self.is_global):
            from Settings import Settings
            return Settings.GLOBAL_SETTINGS[self.name]
        return self.__value
    
    def set_value(self, value):
        self.__value = value
    


# Implement new Variables here
# Each Variable must have a static property called "name" and "text"
# The name MUST start with a small letter
# You can use arguments which must be seperated with a semicolon e.g.: [$your_variable:arg1;arg2]
# Arguments will be passed to init method as a list 

class Date(VariableBase):
    name = 'date'
    
    def __init__(self, args):
        try:
            super().__init__(value=str(datetime.date()) if len(args) == 0 else args[0])
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")

    def get_value(self):
        if(self.recalculate_on_get):
            return str(datetime.date())
        return super().get_value()
    
class DateTime(VariableBase):
    name = 'datetime'

    def __init__(self, args):
        try:
            super().__init__(value=str(datetime.now()) if len(args) == 0 else args[0])
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")

    def get_value(self):
        if(self.recalculate_on_get):
            return str(datetime.now())
        return super().get_value()
    
class Constant(VariableBase):
    name = 'const'

    def __init__(self, args):
        try:
            import Util
            if len(args) == 0:
                raise Exception("No constant name specified!")
            super().__init__(value=Util.get_constant(args[0]))
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")
    
    
class CurrentTaskName(VariableBase):
    name = 'current_task_name'

    def __init__(self):
        try:
            super().__init__(is_global=False)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")
    
class CurrentFileName(VariableBase):
    name = 'current_file_name'

    def __init__(self, args=None):
        try:
            self.with_file_extension = True
            self.with_quotes_around = False
            true_values = ['true', '1', 't', 'y', 'yes', '-1']
            try: self.with_file_extension = args[0].lower() in true_values 
            except: pass
            try: self.with_quotes_around = args[1].lower() in true_values 
            except: pass
            super().__init__(is_global=False)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")
    
    def get_value(self, iterator):
        current_value = iterator.get_current_value() 
        if self.with_file_extension:
            current_value = Path(current_value).name
        else:
            current_value = Path(current_value).stem
        if self.with_quotes_around:
            current_value = f'"{current_value}"'
        return current_value


class CurrentValue(VariableBase):
    name = 'current_value'

    def __init__(self):
        try:
            super().__init__(is_global=False)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")

    def set_value(self, iterator):
        super().set_value(iterator.current_value)
        
class InstallPath(VariableBase):
    name = 'install_path'

    def __init__(self):
        try:
            from Settings import Settings
            super().__init__(value=Settings.INSTALL_PATH)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")