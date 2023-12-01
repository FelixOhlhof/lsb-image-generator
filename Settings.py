import os
import Util

class Settings:
    def load_global_settings():
        Settings.CURRENT_DIR = os.getcwd()
        Settings.INSTALL_PATH = os.path.dirname(__file__)
        Settings.INI_FILE_NAME = "tasks.ini"
        Settings.INI_FILE_SECTION_SETTINGS = "Settings"
        Settings.INI_FILE_SECTION_MODULES = "Modules"
        Settings.INI_FILE_SYSTEM_SECTIONS = [
            Settings.INI_FILE_SECTION_SETTINGS,
            Settings.INI_FILE_SECTION_MODULES
        ]
        Settings.INI_FILE_SETTINGS_RUN_TASKS_PARALLEL = "run_tasks_parallel"
        Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL = "run_commands_parallel"
        Settings.INI_FILE_SETTINGS_COMMAND_AGENT = "command_agent"
        Settings.INI_FILE_SETTINGS_REPORT_AGENT = "report_agent"
        Settings.INI_FILE_SETTINGS_PARAMETER = [
            Settings.INI_FILE_SETTINGS_RUN_TASKS_PARALLEL,
            Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL,
            Settings.INI_FILE_SETTINGS_COMMAND_AGENT,
            Settings.INI_FILE_SETTINGS_REPORT_AGENT
        ]
        Settings.INI_FILE_TASK_COMMAND = "command"
        Settings.INI_FILE_TASK_REPORT = "report"
        Settings.INI_FILE_TASK_PARAMETER = [
            Settings.INI_FILE_TASK_COMMAND,
            Settings.INI_FILE_TASK_REPORT
        ]
        Settings.CURRENT_INI_FILE = f"{Settings.CURRENT_DIR}\\{Settings.INI_FILE_NAME}"
        Settings.BASE_INI_FILE = f"{Settings.INSTALL_PATH}\\{Settings.INI_FILE_NAME}"

        Settings.GLOBAL_SETTINGS = dict()

        true_dict = ['true', '1', 't', 'y', 'yes', '-1']
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_RUN_TASKS_PARALLEL] = Util.get_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_RUN_TASKS_PARALLEL).lower() in true_dict
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL] = Util.get_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL).lower() in true_dict
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_COMMAND_AGENT] = Util.get_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_COMMAND_AGENT).lower() in true_dict
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_REPORT_AGENT] = Util.get_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_REPORT_AGENT).lower() in true_dict


    def __init__(self):
        self.__local_settings = dict()

    def get_value(self, setting_name):
        return self.__local_settings[setting_name]
    
    def add_value(self, key, value):
        self.__local_settings[key] = value