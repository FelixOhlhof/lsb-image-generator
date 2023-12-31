import os
import Util
import configparser

class Settings:
    """Stores static settings."""
    CURRENT_DIR = os.getcwd()
    INSTALL_PATH = os.path.dirname(__file__)
    INI_FILE_NAME = "tasks.ini"
    CURRENT_INI_FILE = os.path.join(CURRENT_DIR, INI_FILE_NAME)
    BASE_INI_FILE = os.path.join(INSTALL_PATH, INI_FILE_NAME)
    INI_FILE = configparser.ConfigParser()
    INI_FILE.read(CURRENT_INI_FILE)
    INI_FILE_SECTION_SETTINGS = "Settings"
    INI_FILE_SECTION_MODULES = "Constants"
    INI_FILE_SYSTEM_SECTIONS = [
        INI_FILE_SECTION_SETTINGS,
        INI_FILE_SECTION_MODULES
    ]
    INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL = "run_commands_parallel"
    INI_FILE_SETTINGS_MAX_PARALLEL_COMMANDS = "max_parallel_commands"
    INI_FILE_SETTINGS_MAX_COMMAND_TIMEOUT_IN_SECONDS = "max_command_timeout_in_seconds"
    INIT_COMMANDS_LAZY = "init_commands_lazy"
    INI_FILE_SETTINGS_COMMAND_AGENT = "command_agent"
    INI_FILE_SETTINGS_REPORT_AGENT = "report_agent"
    INI_FILE_SETTINGS_LOG_FILE_NAME = "log_file_name"
    INI_FILE_SETTINGS_REPORT_FILE_NAME = "report_file_name"
    INI_FILE_TASK_COMMAND = "command"
    INI_FILE_COMMAND_NAME_PATTERN = rf"{INI_FILE_TASK_COMMAND}[0-9]*"
    INI_FILE_TASK_REPORT = "report"
    COMMAND_STATUS_SUCCESS = "Successful"
    COMMAND_STATUS_ERROR = "Error"
    ENABLE_LOG = "enable_log"
    ENABLE_REPORT = "enable_report"

    GLOBAL_SETTINGS = dict()
    
    def load_global_settings():
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL] = Util.get_bool_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL)
        Settings.GLOBAL_SETTINGS[Settings.INIT_COMMANDS_LAZY] = Util.get_bool_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INIT_COMMANDS_LAZY)
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_MAX_PARALLEL_COMMANDS] = Util.get_int_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_MAX_PARALLEL_COMMANDS)
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_MAX_COMMAND_TIMEOUT_IN_SECONDS] = Util.get_int_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_MAX_COMMAND_TIMEOUT_IN_SECONDS)
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_COMMAND_AGENT] = Util.get_bool_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_COMMAND_AGENT)
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_REPORT_AGENT] = Util.get_bool_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_REPORT_AGENT)
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_LOG_FILE_NAME] = Util.get_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_LOG_FILE_NAME)
        Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_REPORT_FILE_NAME] = Util.get_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.INI_FILE_SETTINGS_REPORT_FILE_NAME)
        Settings.GLOBAL_SETTINGS[Settings.ENABLE_LOG] = Util.get_bool_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.ENABLE_LOG)
        Settings.GLOBAL_SETTINGS[Settings.ENABLE_REPORT] = Util.get_bool_value_from_ini_file(Settings.INI_FILE_SECTION_SETTINGS, Settings.ENABLE_REPORT)


    def __init__(self):
        self.__local_settings = dict()

    def get_value(self, setting_name):
        return self.__local_settings[setting_name]
    
    def add_value(self, key, value):
        self.__local_settings[key] = value