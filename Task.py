class Task:
    def __init__(self, name, commands):
        self.name = name
        self.commands = commands

    def run_commands_single_threaded(self):
        for command in self.commands:
            command.execute_all_command_variations()