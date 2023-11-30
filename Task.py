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

    def run_commands_single_threaded(self, runJustFirstCommand = False):
        for command_agent in self.command_agents:
            command_agent.run(runJustFirstCommand)

    def report(self):
        self.report_agent.report()