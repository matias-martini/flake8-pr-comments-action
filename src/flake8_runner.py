import subprocess
import json


class Flake8Runner:
    def __init__(self, source_path=None, config_location_path=None):
        self.command_list = ["flake8", "--format=json"]
        if source_path:
            self.command_list.append(source_path)
        if config_location_path:
            self.command_list.append(f"--config={config_location_path}")

    def run_flake8(self):
        self.completed_process = subprocess.run(self.command_list, stdout=subprocess.PIPE)

    def get_list_of_errors(self):
        errors_by_file_dict = json.loads(self.completed_process.stdout)
        list_of_errors = [item for sublist in errors_by_file_dict.values() for item in sublist]

        return list_of_errors
