import Util
import argparse

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
    if args.action == "run":
        tasks = Util.get_tasks_from_ini_file()
        for task in tasks:
            if args.test:
                task.run_commands_single_threaded(runJustFirstCommand=True)
            else:
                task.run_commands_single_threaded()
    else:
        Util.init()

 


    