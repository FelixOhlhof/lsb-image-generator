from CommandAgent import CommandAgent

class Task:
    def __init__(self, name, commands):
        self.name = name
        self.commands = commands

    def run_commands_single_threaded(self, runJustFirstCommand = False):
        for command in self.commands:
            command_agent = CommandAgent(command)
            command_agent.run(runJustFirstCommand)