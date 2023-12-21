import os
from Settings import Settings
from ProcessItem import ProcessItem
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
        self.finished_processes = []

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
                process = Popen(cmd, stdout=PIPE, shell=True)
                process.wait()
                duration=datetime.now()-start_time
                self.finished_processes.append(ProcessItem(process=None, command_name=self.command.command_name, executed_command=cmd, start_time=start_time, duration=duration))
                if run_just_first_command:
                    return
            except Exception as error:
                self.finished_processes.append(ProcessItem(command_name=self.command.command_name, status=Settings.COMMAND_STATUS_SUCCESS, msg=f"Command: {cmd} raised: {error}", start_time=datetime.now()))

    def __run_parallel(self, run_just_first_command, max_commands, timeout):
        process_queue = Queue(maxsize=max_commands)
        queue_filler = threading.Thread(target=self.__fill_queue_async, args=(run_just_first_command, process_queue,))
        queue_filler.start()
        progress_count = 0
        while self.command.has_next() or not process_queue.empty():
            try:
                processItem = process_queue.get()
                timer = Timer(timeout, self.__handle_timeout, [processItem, timeout, progress_count])
                try:
                    timer.start()
                    processItem.process.wait()
                    endtime = datetime.now()
                    stdout = processItem.process.stdout.read()
                    processItem.status=Settings.COMMAND_STATUS_SUCCESS
                    processItem.msg=stdout
                    processItem.duration=endtime-processItem.start_time
                    processItem.process = None # save some space since it completed successfully
                    self.finished_processes.append(processItem)
                finally:
                    progress_count+=1
                    progress(progress_count, self.command_variants_count, "Running variations:  ")
                    timer.cancel()
            except Exception as e:
                try:
                    processItem.status=Settings.COMMAND_STATUS_ERROR
                    processItem.msg=e
                    processItem.duration=endtime-processItem.start_time
                    self.finished_processes.append(processItem)
                finally:
                    print(f"Fatal Error: {e}")
        queue_filler.join()
        print()
        
    def __handle_timeout(self, processItem, timeout, progress_count):
        processItem.process.kill()
        processItem.status=Settings.COMMAND_STATUS_ERROR
        processItem.msg=f"Command: {processItem.executed_command} timed out after {timeout} seconds."
        self.finished_processes.append(processItem)
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
                process_queue.put(ProcessItem(process=Popen(cmd, stdout=PIPE, shell=True), command_name=self.command.command_name, executed_command=cmd, start_time=datetime.now(), parameter=[[i.name, i.get_current_value()] for i in self.command.iterators]))
                if(run_just_first_command): 
                    break
            except Exception as error:
                print(f"Error while filling command queue async: {error}")
                # self.finished_processes.append(ProcessItem(command_name=self.command.command_name, status=Settings.COMMAND_STATUS_ERROR, msg=error, executed_command=cmd, start_time=datetime.now()))


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('%s[%s] %s\r' % (status, bar, f"{count}/{total}"))
    sys.stdout.flush()
