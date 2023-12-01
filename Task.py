from CommandAgent import CommandAgent
from ReportAgent import ReportAgent

class Task:
    def __init__(self, name, commands):
        self.name = name
        self.commands = commands
        self.command_agents = []
        for command in self.commands:
            self.command_agents.append(CommandAgent(command))
        self.report_agent = ReportAgent(self)

    def run(self, run_just_first_command=False, run_commands_parallel=False):
        for command_agent in self.command_agents:
            command_agent.run(run_just_first_command, run_commands_parallel)

    def report(self):
        self.report_agent.report()