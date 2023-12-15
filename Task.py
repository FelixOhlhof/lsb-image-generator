from CommandAgent import CommandAgent
from datetime import datetime

class Task:
    """
    Represents a Task from the ini file
    """
    def __init__(self, name, commands):
        self.name = name
        self.command_agents = []
        for command in commands:
            self.command_agents.append(CommandAgent(command))

    def run(self, run_just_first_command=False, run_commands_parallel=False, max_commands=10, timeout=10):
        self.start_time = datetime.now()
        print(f"Running {self.name}")
        for command_agent in self.command_agents:
            print(f"Running {command_agent.command.command_name}: {command_agent.command.command_text}")
            command_agent.run(run_just_first_command, run_commands_parallel, max_commands, timeout)
        self.duration = datetime.now()-self.start_time