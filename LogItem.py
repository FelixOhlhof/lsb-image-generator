class LogItem:
    def __init__(self, **kwargs):
        self.time = kwargs.get('time', None)
        self.status = kwargs.get('status', None)
        self.executed_command = kwargs.get('executed_command', None)
        self.msg = kwargs.get('msg', None)