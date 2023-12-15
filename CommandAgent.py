import os
from Settings import Settings
from LogItem import LogItem
from subprocess import Popen, PIPE
from queue import Queue
import threading
import time
from datetime import datetime
import sys
from threading import Timer

class CommandAgent:
    """
    Standard implementation for consuming an command in a given way. 
    """
    def __init__(self, command):
        self.command = command
        self.command_variants_count = self.command.command_queue.qsize()
        self.logs = []

    def run(self, run_just_first_command=False, run_commands_parallel=False, max_commands=10, timeout=10):
        try:
            if run_commands_parallel:
                self.__run_parallel(run_just_first_command, max_commands, timeout)
            else:
                self.__run_sequential(run_just_first_command)
        except Exception as error:
            print(f"Error while executing command agent: {error}")
    
    def __run_sequential(self, run_just_first_command):
        while self.command.has_next():
            cmd = ""
            try:
                cmd = self.command.get_next()
                start_time = datetime.now()
                os.system(cmd)
                self.logs.append(LogItem(command_name= self.command.command_name, status=Settings.COMMAND_STATUS_SUCCESS, executed_command=cmd, start_time=start_time, duration=datetime.now()-start_time))
                if run_just_first_command:
                    return
            except Exception as error:
                self.logs.append(LogItem(command_name= self.command.command_name, status=Settings.COMMAND_STATUS_SUCCESS, msg=f"Command: {cmd} raised: {error}", start_time=datetime.now()))

    def __run_parallel(self, run_just_first_command, max_commands, timeout):
        process_queue = Queue(maxsize=max_commands)
        queue_filler = threading.Thread(target=self.__fill_queue_async, args=(run_just_first_command, process_queue,))
        queue_filler.start()
        progress_count = 0
        while self.command.has_next() or not process_queue.empty():
            try:
                process = process_queue.get()
                timer = Timer(timeout, self.__handle_timeout, [process, timeout, progress_count])
                try:
                    timer.start()
                    process[0].wait()
                    endtime = datetime.now()
                    stdout = process[0].stdout.read()
                    self.logs.append(LogItem(command_name= self.command.command_name, status=Settings.COMMAND_STATUS_SUCCESS, executed_command=process[1], msg=stdout, start_time=process[2], duration=endtime-process[2]))
                finally:
                    progress_count+=1
                    progress(progress_count, self.command_variants_count, "Running variations:  ")
                    timer.cancel()
            except Exception as e:
                self.logs.append(LogItem(command_name= self.command.command_name, status=Settings.COMMAND_STATUS_ERROR, executed_command=process[1], msg=e, start_time=process[2]))
        queue_filler.join()
        print()
        
    def __handle_timeout(self, process, timeout, progress_count):
        process[0].kill()
        self.logs.append(LogItem(status=Settings.COMMAND_STATUS_ERROR, msg=f"Command: {process[1]} timed out after {timeout} seconds."))
        progress_count+=1
        progress(progress_count, self.command_variants_count, "Running variations:  ")

    def __fill_queue_async(self, run_just_first_command, process_queue):
        while self.command.has_next():
            cmd = ""
            try:
                while process_queue.full():
                    time.sleep(0.05)
                    pass
                cmd = self.command.get_next()
                process_queue.put([Popen(cmd, stdout=PIPE, shell=True), cmd, datetime.now()])
                if(run_just_first_command): 
                    break
            except Exception as error:
                self.logs.append(LogItem(command_name= self.command.command_name, status=Settings.COMMAND_STATUS_ERROR, msg=error, executed_command=cmd, start_time=datetime.now()))


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('%s[%s] %s\r' % (status, bar, f"{count}/{total}"))
    sys.stdout.flush()
