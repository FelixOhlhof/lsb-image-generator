class ProcessItem:
    """
    Represents a LogItem.
    The CommandAgent is responsable to instantiate new LogItems. 
    """
    def __init__(self, process, **kwargs):
        self.process = process
        self.start_time = kwargs.get('start_time', None)
        self.duration = kwargs.get('duration', None)
        self.status = kwargs.get('status', None)
        self.command_name = kwargs.get('command_name', None)
        self.executed_command = kwargs.get('executed_command', None)
        self.parameter = kwargs.get('parameter', None)
        self.msg = kwargs.get('msg', None)