import os
import csv
from datetime import datetime

class ReportAgent:
    def __init__(self, task):
        self.task = task

    def report(self):
        import Util
        f = open(f"{Util.CURRENT_DIR}\\report.csv", "a")
        f.write(f"[{self.task.name}]    {datetime.now()}")
    
        for command_agent in self.task.command_agents:
            cmd_nr = self.task.command_agents.index(command_agent) + 1
            f.write(f"\nCommand {cmd_nr}: ")
            while not command_agent.log_queue.empty():
                f.write(f"{command_agent.log_queue.get()}\n")
        f.write(f"\n")
        f.close()