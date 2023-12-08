import Util
import argparse
from multiprocessing import Process, Queue
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

 
def run_tasks_sequential(tasks):
    for task in tasks:
        task.run(run_just_first_command=args.test, run_commands_parallel=Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL])
        task.report()
     
def run_tasks_parallel(tasks):
    procs = []
    for i in range(0, len(tasks)):
        task = tasks[i]
        proc = Process(target=task.run, args=(args.test, Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_RUN_COMMANDS_PARALLEL], Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_MAX_PARALLEL_COMMANDS], Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_MAX_COMMAND_TIMEOUT_IN_SECONDS]))
        procs.append(proc)
        proc.start()
        if i % Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_MAX_PARALLEL_TASKS] == 0 and i != 0:
            print("Started 10 Tasks")
            for proc in procs:
                proc.join()
            procs = []
    for proc in procs:
        proc.join()   
    pass

if __name__=="__main__":
    if args.action == "run":
        Settings.load_global_settings()
        tasks = Util.get_tasks_from_ini_file()
        if(Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_RUN_TASKS_PARALLEL]):
            run_tasks_parallel(tasks)
        else:
            run_tasks_sequential(tasks)
        report_agent = ReportAgent(tasks)
        if Settings.GLOBAL_SETTINGS[Settings.ENABLE_REPORT]:
            report_agent.create_report()
        if Settings.GLOBAL_SETTINGS[Settings.ENABLE_LOG]:
            report_agent.create_log()
    elif args.action == "init":
        Util.init()


