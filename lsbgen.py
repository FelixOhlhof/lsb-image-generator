import Util
import argparse
from Settings import Settings

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

if __name__=="__main__":
    Settings.load_global_settings()

    if args.action == "run":
        tasks = Util.get_tasks_from_ini_file()
        for task in tasks:
            task.run(run_just_first_command=args.test, run_commands_parallel=Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL])
            task.report()
    else:
        Util.init()

 


    