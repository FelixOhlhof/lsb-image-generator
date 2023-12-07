import os
from Settings import Settings
from LogItem import LogItem
from subprocess import Popen, PIPE

class CommandAgent:
    def __init__(self, command):
        self.command = command
        self.command_variants_count = self.command.command_queue.qsize()

    def run(self, logs, run_just_first_command=False, run_commands_parallel=False):
        if run_commands_parallel:
            self.__run_parallel(logs, run_just_first_command)
        else:
            self.__run_sequential(logs, run_just_first_command)
    
    def __run_sequential(self, logs, run_just_first_command):
        while self.command.has_next():
            cmd = ""
            try:
                cmd = self.command.get_next()
                os.system(cmd)
                logs.append(LogItem(status=Settings.COMMAND_STATUS_SUCCESS, msg=cmd))
                if run_just_first_command:
                    return
            except Exception as error:
                logs.append(LogItem(status=Settings.COMMAND_STATUS_SUCCESS, msg=f"Command: {cmd} raised: {error}"))

    def __run_parallel(self, logs, run_just_first_command):
        processes = []

        while self.command.has_next():
            cmd = ""
            try:
                cmd = self.command.get_next()
                processes.append([Popen(cmd, stdout=PIPE), cmd])
                if(run_just_first_command): 
                    break
            except Exception as error:
                logs.append(LogItem(status=Settings.COMMAND_STATUS_ERROR, msg=f"Command: {cmd} raised: {error}"))
        for proc in processes:
            proc[0].wait()
            stdout = proc[0].stdout.read()
            logs.append(LogItem(status=Settings.COMMAND_STATUS_SUCCESS,executed_command=proc[1],  msg=stdout))
        print()