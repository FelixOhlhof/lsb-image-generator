import os

class CommandAgent:
    def __init__(self, command):
        self.command = command

    def run(self):
        while self.command.has_next():
            # report extensions/agent comes here
            os.system(self.command.get_next())