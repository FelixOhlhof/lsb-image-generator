import os
from multiprocessing import Queue
from subprocess import Popen, PIPE

class CommandAgent:
    def __init__(self, command):
        self.command = command
        self.log_queue = Queue()
        self.procs = []

    def run(self, run_just_first_command=False, run_commands_parallel=False):
        if run_commands_parallel:
            self.__run_parallel(run_just_first_command)
        else:
            self.__run_sequential(run_just_first_command)
    
    def __run_sequential(self, run_just_first_command):
        while self.command.has_next():
            cmd = ""
            try:
                cmd = self.command.get_next()
                os.system(cmd)
                self.log_queue.put(cmd)
                if run_just_first_command:
                    return
            except Exception as error:
                self.log_queue.put(f"Error: {error} in command {cmd}")

    def __run_parallel(self, run_just_first_command):
        while self.command.has_next():
            cmd = ""
            try:
                cmd = self.command.get_next()
                self.procs.append(Popen(cmd, stdout=PIPE, stderr=PIPE))
                if(run_just_first_command): 
                    break
            except Exception as error:
                self.log_queue.put(f"Error: {error} in command {cmd}")
        for proc in self.procs:
            proc.wait()
            stdout = proc.stdout.read()
            stderr = proc.stderr.read()
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)
        print()
            
