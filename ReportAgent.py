from Settings import Settings
from datetime import datetime
import Util
import os
import csv

class ReportAgent:
    """
    Standard implementation for creating a report and log file. 
    """
    def __init__(self, tasks):
        self.tasks = tasks

    def create_report(self):
        with open(os.path.join(Settings.CURRENT_DIR, Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_REPORT_FILE_NAME]), "a") as file:
            file.write(f"Report created at: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
            for task in self.tasks:
                rpt = []
                for command_agent in task.command_agents:
                    successfull = [process_item.status for process_item in command_agent.finished_processes].count(Settings.COMMAND_STATUS_SUCCESS)
                    error = [process_item.status for process_item in command_agent.finished_processes].count(Settings.COMMAND_STATUS_ERROR)
                    rpt.append((command_agent.command.command_name, successfull, error))
                
                file.write(f"\n{task.name} -> Execution timestamp: {task.start_time}  Duration: {task.duration}  Total command variations: {len([c[1] + c[2] for c in rpt])}  Total successfull: {len([c[1] for c in rpt])}  Total errors: {len([c[2] for c in rpt])}\n")
                for cmd_rpt in rpt:
                    file.write(f"{cmd_rpt[0]} -> Successfull: {cmd_rpt[1]}  Errors: {cmd_rpt[2]}\n")

            file.write(f"\n\nConfig:\n")
            file.write(f"{Util.get_complete_section_string(Settings.INI_FILE_SECTION_SETTINGS)}\n")
            file.write(f"{Util.get_complete_section_string(Settings.INI_FILE_SECTION_MODULES)}\n")
            file.write(f"{Util.get_complete_task_section_string()}\n")
        print("Created report")

    def create_log(self):
        with open(os.path.join(Settings.CURRENT_DIR, Settings.GLOBAL_SETTINGS[Settings.INI_FILE_SETTINGS_LOG_FILE_NAME]), "a", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Task Name", "Command Name", "Execution timestamp", "Duration", "Status", "Executed Command", "Output Message"])
            for task in self.tasks:
                for command_agent in task.command_agents:
                    for process_item in command_agent.finished_processes:
                        row = [task.name, command_agent.command.command_name, process_item.start_time, process_item.duration, process_item.status, process_item.executed_command, process_item.msg]
                        if(process_item.parameter):
                            for p in process_item.parameter:
                                row.append(f"{p[0]}:")
                                row.append(p[1])
                        writer.writerow(row)
        print("Created log file")
