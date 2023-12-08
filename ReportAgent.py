from Settings import Settings
from datetime import datetime
import Util
import os

class ReportAgent:
    def __init__(self, tasks):
        self.tasks = tasks

    def create_report(self):
        f = open(os.path.join(Settings.CURRENT_DIR, Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_REPORT_FILE_NAME]), "a")
        f.write(f"Report created at: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        f.write(f"Total tasks: {len(self.tasks)} ")
        for t in self.tasks:
            f.write(f"{t.name} commands executed: {sum(i.command_variants_count for i in t.command_agents)}  Successfull: {len((l for l in i.log if l.status == Settings.COMMAND_STATUS_SUCCESS) for i in t.command_agents)}  Errors: {sum(l for l in t.log if l.status == Settings.COMMAND_STATUS_ERROR for i in t.command_agents)}")
            
        f.write(f"Config:\n")
        f.write(f"{Util.get_complete_section_string(Settings.INI_FILE_SECTION_SETTINGS)}\n")
        f.write(f"{Util.get_complete_section_string(Settings.INI_FILE_SECTION_MODULES)}\n")
        f.write(f"{Util.get_complete_task_section_string()}\n")
    
        f.write(f"\n")
        f.close()

    def create_log(self):
        f = open(os.path.join(Settings.CURRENT_DIR, Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_LOG_FILE_NAME]), "a")
        f.write(f"Created log at {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
    
        for task in self.tasks:
            f.write(f"Task {task.name}: \n")
            while not task.multi_process_log_queue.empty():
                log_item = task.multi_process_log_queue.get()
                f.write(f"Executed command: {log_item.executed_command}\nStatus: {log_item.status}\n")
                f.write(f"Output: {log_item.msg}\n\n")
            # for command_agent in task.command_agents:
            #     cmd_nr = task.command_agents.index(command_agent) + 1
            #     f.write(f"\nCommand {cmd_nr}: stderr")
            #     for log in command_agent.logs:
            #         f.write(f"{log}\n")
            # f.write(f"\n")
        f.close()