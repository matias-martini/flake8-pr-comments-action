import json
import requests


class GithubClient:
    def __init__(self, gh_token, gh_commit, gh_repo_owner, gh_repo_name, gh_pull_request_id):
        self.gh_token = gh_token
        self.gh_commit = gh_commit
        self.gh_repo_owner = gh_repo_owner
        self.gh_repo_name = gh_repo_name
        self.gh_pull_request_id = gh_pull_request_id

        self.request_header = self._get_request_header()
        self.base_url_for_requests = self._get_base_url_for_requests()

    def list_changed_python_files_in_pr(self):
        response = requests.get(
            f"{self.base_url_for_requests}/files",
            headers=self.request_header,
        )

        if response.status_code != 200:
            raise Exception(
                f"Error '{response.status_code}' while retrieving files "
                "affected in the Pull Request."
            )

        files_data_list = json.loads(response.content)
        files_name_list = map(lambda file_data: file_data["filename"], files_data_list)
        python_files_list = filter(lambda file_name: file_name.endswith(".py"), files_name_list)

        return list(python_files_list)

    def send_pr_review_comment(self, file_path, line_to_comment, message):
        response = requests.post(
            f"{self.base_url_for_requests}/comments",
            headers=self.request_header,
            data=json.dumps(
                {
                    "body": message,
                    "commit_id": self.gh_commit,
                    "path": file_path,
                    "line": line_to_comment,
                    "side": "RIGHT"
                 })
        )

        if response.status_code in [200, 201]:
            return

        raise Exception(response.status_code)

    def _get_request_header(self):
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.gh_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def _get_base_url_for_requests(self):
        return f"https://api.github.com/repos/{self.gh_repo_owner}/{self.gh_repo_name}/pulls/{self.gh_pull_request_id}"  # noqa: E501
