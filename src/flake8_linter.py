import subprocess
import json


class Flake8Linter:
    def __init__(self, config_location_path=None):
        self.base_command_list = ["flake8", "--format=json"]
        if config_location_path:
            self.base_command_list.append(f"--config={config_location_path}")

    def get_list_of_errors(self, file_path=None):
        self.run_flake8(file_path=file_path)

        try:
            errors_by_file_dict = json.loads(self.completed_process.stdout)
            list_of_errors = [item for sublist in errors_by_file_dict.values() for item in sublist]

            return list_of_errors
        except Exception:
            return []

    def run_flake8(self, file_path=None):
        command_list = self.base_command_list.copy()
        if file_path:
            command_list.append(file_path)

        print("Flake8 ran as:")
        print(f"\t'{' '.join(command_list)}'")

        self.completed_process = subprocess.run(
            command_list,
            stdout=subprocess.PIPE
        )
