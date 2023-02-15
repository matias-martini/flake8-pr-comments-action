import os
from flake8_linter import Flake8Linter
from github_client import GithubClient

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_COMMIT = os.environ["GITHUB_COMMIT"]
GITHUB_OWNER = os.environ["GITHUB_OWNER"]
GITHUB_REPO = os.environ["GITHUB_REPO"]
GITHUB_PULL_NUMBER = os.environ["GITHUB_PULL_NUMBER"]
FLAKE8_CFG_PATH = os.environ["FLAKE8_CFG_PATH"]


def run_linter_and_comment_errors():
    flake8_linter = Flake8Linter(config_location_path=FLAKE8_CFG_PATH)

    github_client = GithubClient(
        GITHUB_TOKEN, GITHUB_COMMIT, GITHUB_OWNER, GITHUB_REPO, GITHUB_PULL_NUMBER
    )

    changed_files_in_pr = github_client.list_changed_python_files_in_pr()

    for file_path in changed_files_in_pr:
        list_of_errors = flake8_linter.get_list_of_errors(file_path=file_path)

        for error_data in list_of_errors:
            line_number, message = get_line_and_message(error_data)

            try:
                github_client.send_pr_review_comment(file_path, line_number, message)
            except Exception as e:
                print(f"Error code '{e}' while trying to send PR comment")
                print(e)


def get_line_and_message(error_data):
    error_code, file_name, line_number, _, text, _ = error_data.values()
    message = f"**[{error_code}]** -> {text.capitalize()}"

    return line_number, message


if __name__ == "__main__":
    run_linter_and_comment_errors()
