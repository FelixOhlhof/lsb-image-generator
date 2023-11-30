import os
import queue

class CommandAgent:
    def __init__(self, command):
        self.command = command
        self.log_queue = queue.Queue()


    def run(self, runJustFirstCommand=False):
        while self.command.has_next():
            cmd = ""
            try:
                cmd = self.command.get_next()
                os.system(cmd)
                self.log_queue.put(cmd)
                if runJustFirstCommand:
                    return
            except Exception as error:
                self.log_queue.put(f"Error: {error} in command {cmd}")
