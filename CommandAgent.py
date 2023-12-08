import os
from Settings import Settings
from LogItem import LogItem
from subprocess import Popen, PIPE
from multiprocessing import Queue
import threading
import time

class CommandAgent:
    def __init__(self, command):
        self.command = command
        self.command_variants_count = self.command.command_queue.qsize()

    def run(self, logs, run_just_first_command=False, run_commands_parallel=False, max_commands=10, timeout=10):
        if run_commands_parallel:
            self.__run_parallel(logs, run_just_first_command, max_commands, timeout)
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

    def __run_parallel(self, logs, run_just_first_command, max_commands, timeout):
        process_queue = Queue(maxsize=max_commands)

        queue_filler = threading.Thread(target=self.__fill_queue_async, args=(logs, run_just_first_command, process_queue,))
        queue_filler.start()

        while queue_filler.is_alive():
            process = process_queue.get()
            process[0].wait()
            stdout = process[0].stdout.read()
            logs.append(LogItem(status=Settings.COMMAND_STATUS_SUCCESS, executed_command=process[1], msg=stdout))
        

    def __fill_queue_async(self, logs, run_just_first_command, process_queue):
        while self.command.has_next():
            cmd = ""
            try:
                while process_queue.full():
                    time.sleep(0.1) 
                cmd = self.command.get_next()
                process_queue.put([Popen(cmd, stdout=PIPE), cmd])
                if(run_just_first_command): 
                    break
            except Exception as error:
                logs.append(LogItem(status=Settings.COMMAND_STATUS_ERROR, msg=f"Command: {cmd} raised: {error}"))
        print()