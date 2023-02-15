import subprocess
import json
from send_pr_comment import SendPrComment
import os

SRC_PATH = os.environ["FLAKE8_SRC_PATH"]
CFG_PATH = os.environ["FLAKE8_CFG_PATH"]

command_list = ["flake8", "--format=json"]
if CFG_PATH: command_list.append(f"--config={CFG_PATH}")

result = subprocess.run(command_list, stdout=subprocess.PIPE)
errors = json.loads(result.stdout)

for file_path_errors in errors.values():
    for error in file_path_errors:
        error_code, file_name, line_number, _, text, _ = error.values()
        message = f"[{error_code}] -> {text}"

        response = SendPrComment(file_name, line_number, message).perform()
