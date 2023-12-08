import Util
import argparse
import sys
from queue import Queue
from Settings import Settings
from ReportAgent import ReportAgent

argParser = argparse.ArgumentParser(prog='lsbgen',
                    description='Generate LSB Images',
                    epilog='...')
ActionHelp = """
    run = Run all tasks all commands
    init = Initialize new workspace
    """
argParser.add_argument('action', choices=('run', 'init'), help = ActionHelp)
argParser.add_argument('-t', '--test', action='store_true', help="Run test: all tasks but just first command/variation")
args = argParser.parse_args()
     
def run_tasks(tasks):
    for t in tasks:
        t.run(args.test, Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL], Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_MAX_PARALLEL_COMMANDS], Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_MAX_COMMAND_TIMEOUT_IN_SECONDS])
    print("All tasks completed")
    
if __name__=="__main__":   
    if args.action == "run":
        Settings.load_global_settings()
        tasks = Util.get_tasks_from_ini_file()
        run_tasks(tasks)
        report_agent = ReportAgent(tasks)
        if Settings.GLOBAL_SETTINGS[Settings.ENABLE_REPORT]:
            report_agent.create_report()
        if Settings.GLOBAL_SETTINGS[Settings.ENABLE_LOG]:
            report_agent.create_log()
    elif args.action == "init":
        Util.init()


