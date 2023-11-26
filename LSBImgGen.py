import Util

if __name__=="__main__":
    tasks = Util.get_tasks_from_ini_file('tasks.ini')
    for task in tasks:
        task.run_commands_single_threaded()