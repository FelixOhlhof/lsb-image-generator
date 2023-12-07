from datetime import datetime   
from pathlib import Path

class VariableBase:
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
    text = ''
    
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
    text = ''

    def __init__(self, args):
        try:
            super().__init__(value=str(datetime.now()) if len(args) == 0 else args[0])
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")

    def get_value(self):
        if(self.recalculate_on_get):
            return str(datetime.now())
        return super().get_value()
    
class ModuleRunCommand(VariableBase):
    name = 'module_cmd'
    text = ''

    def __init__(self, args):
        try:
            import Util
            if len(args) == 0:
                raise Exception("No module name specified!")
            super().__init__(value=Util.get_module_cmd(args[0]))
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")
    
    
class CurrentTaskName(VariableBase):
    name = 'current_task_name'
    text = ''

    def __init__(self):
        try:
            super().__init__(is_global=False)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")
    
class CurrentFilePath(VariableBase):
    name = 'current_file_path'
    text = ''

    def __init__(self):
        try:
            super().__init__(is_global=False)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")
    
    def set_value(self, iterator):
        super().set_value(iterator.current_value)
    
class CurrentFileName(VariableBase):
    name = 'current_file_name'
    text = ''

    def __init__(self, *args):
        try:
            self.without_extension = False
            if len(args) != 0:
                self.without_extension = bool(args[0])
            super().__init__(is_global=False)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")
    
    def set_value(self, iterator):
        super().set_value(Path(iterator.current_value).stem if self.without_extension else Path(iterator.current_value).name)

class CurrentValue(VariableBase):
    name = 'current_value'
    text = ''

    def __init__(self):
        try:
            super().__init__(is_global=False)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")

    def set_value(self, iterator):
        super().set_value(iterator.current_value)

class CurrentModuleName(VariableBase):
    name = 'current_module_name'
    text = ''

    def __init__(self):
        try:
            super().__init__(is_global=False)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")
        
class InstallPath(VariableBase):
    name = 'install_path'
    text = ''

    def __init__(self):
        try:
            from Settings import Settings
            super().__init__(value=Settings.INSTALL_PATH)
        except Exception as error:
            raise Exception(f"Could not initialize {self.name} Variable: {error}")