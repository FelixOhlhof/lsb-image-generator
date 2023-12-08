from CommandAgent import CommandAgent
from ReportAgent import ReportAgent
from multiprocessing import Queue

class Task:
    def __init__(self, name, commands):
        self.name = name
        self.command_agents = []
        self.multi_process_log_queue = Queue()
        for command in commands:
            self.command_agents.append(CommandAgent(command))

    def run(self, run_just_first_command=False, run_commands_parallel=False, max_commands=10, timeout=10):
        print(f"Running {self.name}")
        logs = []
        for command_agent in self.command_agents:
            print(f"Running {command_agent.command.command_name}: {command_agent.command.command_text}")
            command_agent.run(logs, run_just_first_command, run_commands_parallel, max_commands, timeout)
        for l in logs:
            self.multi_process_log_queue.put(l)
        pass