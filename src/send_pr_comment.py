import json
import requests
import os

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_COMMIT = os.environ["GITHUB_COMMIT"]
GITHUB_OWNER = os.environ["GITHUB_OWNER"]
GITHUB_REPO = os.environ["GITHUB_REPO"]
GITHUB_PULL_NUMBER = os.environ["GITHUB_PULL_NUMBER"]

URI = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls/{GITHUB_PULL_NUMBER}/comments"

HEADER = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}


class SendPrComment:
    def __init__(self, file_path, line_to_comment, message):
        self.line_to_comment = line_to_comment
        self.message = message
        self.file_path = self.sanitize_path(file_path)

    def sanitize_path(self, path):
        if path.startswith("./"):
            return path[2:]
        return path

    def perform(self):
        print(URI)
        print(HEADER)
        print(json.dumps(self.get_payload()))
        response = requests.post(
            URI,
            headers=HEADER,
            data=json.dumps(self.get_payload())
        )

        return response

    def get_payload(self):
        return {
            "body": self.message,
            "commit_id": GITHUB_COMMIT,
            "path": self.file_path,
            "line": self.line_to_comment,
            "side": "RIGHT"
        }
